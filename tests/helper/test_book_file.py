import os
import tempfile
from unittest.mock import patch

import pytest
from fastapi import UploadFile

from app.helper.book_file import get_basename, is_file_exists, remove_file, save_file


@pytest.mark.asyncio
async def test_save_file_creates_file():
    tmp_file = tempfile.NamedTemporaryFile(delete=False)
    tmp_file.write(b"Test content")
    tmp_file.seek(0)

    with open(tmp_file.name, "rb") as f:
        upload_file = UploadFile(filename="testfile.txt", file=f)

        saved_path = save_file(upload_file)

        assert os.path.exists(saved_path)

        with open(saved_path, "rb") as saved_file:
            content = saved_file.read()
            assert content == b"Test content"

    # Clean up
    os.remove(saved_path)
    tmp_file.close()
    os.remove(tmp_file.name)


def test_is_file_exists_true_and_false(tmp_path):
    existing_file = tmp_path / "existing_file.txt"
    existing_file.write_text("Test")

    # Exists
    assert is_file_exists(str(existing_file)) is True

    # Does not exist
    non_existing_file = tmp_path / "non_existing.txt"
    assert is_file_exists(str(non_existing_file)) is False

    # Empty path
    assert is_file_exists("") is False


def test_get_basename():
    path = "/some/random/path/file.txt"
    result = get_basename(path)
    assert result == "file.txt"


def test_remove_file_when_exists(tmp_path):
    test_file = tmp_path / "file_to_remove.txt"
    test_file.write_text("To be removed")

    # Check file exists
    assert os.path.exists(test_file)

    remove_file(str(test_file))

    # Check file removed
    assert not os.path.exists(test_file)


def test_remove_file_when_not_exists():
    with (
        patch("app.helper.book_file.is_file_exists") as mock_exists,
        patch("os.remove") as mock_remove,
    ):
        mock_exists.return_value = False

        remove_file("/fake/path/to/file.txt")

        mock_remove.assert_not_called()
