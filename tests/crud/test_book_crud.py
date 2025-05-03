from http import HTTPStatus
from unittest.mock import AsyncMock, MagicMock, patch

import pytest
from fastapi import HTTPException

from app.crud.book import delete_book, fetch_book, list_books, save_book, update_book
from app.models import Book as BookDBModel
from app.schemas.requests import BookCreate, BookFilter, BookUpdate


@pytest.mark.asyncio
async def test_fetch_book_found(fake_db_session):
    book = BookDBModel(id=1, name="Test Book")
    scalars = MagicMock()
    scalars.first.return_value = book

    fake_db_session.scalars.return_value = scalars

    result = await fetch_book(fake_db_session, 1)
    assert result == book


@pytest.mark.asyncio
async def test_fetch_book_not_found(fake_db_session):
    scalars = MagicMock()
    scalars.first.return_value = None

    fake_db_session.scalars.return_value = scalars

    with pytest.raises(HTTPException) as exc:
        await fetch_book(fake_db_session, 999)

    assert exc.value.status_code == HTTPStatus.NOT_FOUND


@pytest.mark.asyncio
async def test_list_books_found(fake_db_session):
    books = [BookDBModel(id=1, name="Book 1"), BookDBModel(id=2, name="Book 2")]

    scalars = MagicMock()
    scalars.all.return_value = books

    fake_db_session.scalars.return_value = scalars

    filters = BookFilter(
        name=None, author=None, genre=None, date_published=None, limit=10, offset=0
    )

    result = await list_books(fake_db_session, filters)
    assert result == books


@pytest.mark.asyncio
async def test_list_books_not_found(fake_db_session):
    scalars = MagicMock()
    scalars.all.return_value = []

    fake_db_session.scalars.return_value = scalars

    filters = BookFilter(
        name=None, author=None, genre=None, date_published=None, limit=10, offset=0
    )

    with pytest.raises(HTTPException) as exc:
        await list_books(fake_db_session, filters)

    assert exc.value.status_code == HTTPStatus.NOT_FOUND


@pytest.mark.asyncio
async def test_save_book(fake_db_session):
    book_data = BookCreate(
        name="Test Book",
        author="Author",
        genre="Genre",
        date_published="2025-05-02",
    )

    file_path = "/tmp/file.txt"

    result = await save_book(fake_db_session, book_data, file_path)

    fake_db_session.add.assert_called_once()
    fake_db_session.commit.assert_awaited_once()
    fake_db_session.refresh.assert_awaited_once_with(result)

    assert result.name == book_data.name
    assert result.file_path == file_path


@pytest.mark.asyncio
async def test_update_book(monkeypatch, fake_db_session):
    book = BookDBModel(id=1, name="Old Name", file_path="old_file.txt")

    fake_db_session.commit = AsyncMock()
    fake_db_session.refresh = AsyncMock()

    async def fake_fetch_book(db_session, book_id):
        return book

    monkeypatch.setattr("app.crud.book.fetch_book", fake_fetch_book)

    with patch("app.crud.book.remove_file") as mock_remove_file:
        book_data = BookUpdate(name="New Name")

        result = await update_book(fake_db_session, 1, book_data, "new_file.txt")

        assert result.name == "New Name"
        assert result.file_path == "new_file.txt"
        mock_remove_file.assert_called_once_with("old_file.txt")


@pytest.mark.asyncio
async def test_update_book_no_file(monkeypatch, fake_db_session):
    book = BookDBModel(id=1, name="Old Name", file_path="same_file.txt")

    fake_db_session.commit = AsyncMock()
    fake_db_session.refresh = AsyncMock()

    async def fake_fetch_book(db_session, book_id):
        return book

    monkeypatch.setattr("app.crud.book.fetch_book", fake_fetch_book)

    with patch("app.crud.book.remove_file") as mock_remove_file:
        book_data = BookUpdate(name="New Name")

        result = await update_book(fake_db_session, 1, book_data, "same_file.txt")

        assert result.name == "New Name"
        mock_remove_file.assert_not_called()


@pytest.mark.asyncio
async def test_delete_book(monkeypatch, fake_db_session):
    book = BookDBModel(id=1, name="To Delete", file_path="delete_file.txt")

    fake_db_session.commit = AsyncMock()
    fake_db_session.delete = AsyncMock()

    async def fake_fetch_book(db_session, book_id):
        return book

    monkeypatch.setattr("app.crud.book.fetch_book", fake_fetch_book)

    with patch("app.crud.book.remove_file") as mock_remove_file:
        await delete_book(fake_db_session, 1)

        fake_db_session.delete.assert_awaited_once_with(book)
        fake_db_session.commit.assert_awaited_once()
        mock_remove_file.assert_called_once_with("delete_file.txt")
