import os
import shutil
from uuid import uuid4

from fastapi import UploadFile

UPLOAD_DIR = "./uploaded_books"
os.makedirs(UPLOAD_DIR, exist_ok=True)


def save_file(file: UploadFile) -> str:
    file_location = os.path.join(UPLOAD_DIR, f"{uuid4()}_{file.filename}")
    file.file.seek(0)
    with open(file_location, "wb") as buffer:
        shutil.copyfileobj(file.file, buffer)
    return file_location


def is_file_exists(file_path: str) -> bool:
    return bool(file_path) and os.path.exists(file_path)


def get_basename(file_path: str) -> str:
    return os.path.basename(file_path)


def remove_file(file_path: str) -> None:
    if is_file_exists(file_path):
        os.remove(file_path)
