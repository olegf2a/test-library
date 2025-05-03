from unittest.mock import patch

import pytest
from fastapi import status


@pytest.mark.asyncio
async def test_get_book_not_found(async_client):
    response = await async_client.get("/api/books/99999")
    assert response.status_code == status.HTTP_404_NOT_FOUND


@pytest.mark.asyncio
async def test_get_books(async_client):
    response = await async_client.get("/api/books")
    assert response.status_code == status.HTTP_200_OK
    assert isinstance(response.json(), list)


@pytest.mark.asyncio
async def test_create_book(async_client, tmp_path):
    test_file = tmp_path / "testfile.txt"
    test_file.write_text("Book content")

    with patch("app.helper.book_file.save_file") as mock_save_file:
        mock_save_file.return_value = str(test_file)

        with open(test_file, "rb") as file:
            response = await async_client.post(
                "/api/books",
                data={
                    "name": "Test Book",
                    "author": "Test Author",
                    "genre": "Test Genre",
                    "date_published": "2025-05-02",
                },
                files={"file": file},
            )
        assert response.status_code == status.HTTP_200_OK
        data = response.json()
        assert data["name"] == "Test Book"
        assert "id" in data


@pytest.mark.asyncio
async def test_update_book(async_client, tmp_path, upload_file):
    file = upload_file(content=b"My Book", filename="book.txt")

    response = await async_client.post(
        "/api/books",
        data={
            "name": "Updated Book Name",
            "author": "Author",
            "genre": "Fiction",
            "date_published": "2025-05-02",
        },
        files={"file": (file.filename, file.file, "text/plain")},
    )

    assert response.status_code == status.HTTP_200_OK
    assert response.json()["name"] == "Updated Book Name"


@pytest.mark.asyncio
async def test_download_file_not_found(async_client, tmp_path):
    with patch("app.helper.book_file.is_file_exists") as mock_exists:
        mock_exists.return_value = False

        response = await async_client.get("/api/books/99999/download")
        assert response.status_code == status.HTTP_404_NOT_FOUND


@pytest.mark.asyncio
async def test_preview_file_not_found(async_client, tmp_path):
    with patch("app.helper.book_file.is_file_exists") as mock_exists:
        mock_exists.return_value = False

        response = await async_client.get("/api/books/99999/preview")
        assert response.status_code == status.HTTP_404_NOT_FOUND


@pytest.mark.asyncio
async def test_delete_book(async_client, tmp_path):
    test_file = tmp_path / "testfile_delete.txt"
    test_file.write_text("Delete Book content")

    with patch("app.helper.book_file.save_file") as mock_save_file:
        mock_save_file.return_value = str(test_file)

        with open(test_file, "rb") as file:
            response = await async_client.post(
                "/api/books",
                data={
                    "name": "Book to Delete",
                    "author": "Author",
                    "genre": "Genre",
                    "date_published": "2025-05-02",
                },
                files={"file": file},
            )
        book_id = response.json()["id"]

        response = await async_client.delete(f"/api/books/{book_id}")
        assert response.status_code == status.HTTP_204_NO_CONTENT

        response = await async_client.get(f"/api/books/{book_id}")
        assert response.status_code == status.HTTP_404_NOT_FOUND
