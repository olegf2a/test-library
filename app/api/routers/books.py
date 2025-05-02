from collections.abc import Sequence
from typing import Annotated

from fastapi import APIRouter, Depends, File, HTTPException, UploadFile
from fastapi.responses import FileResponse
from starlette.datastructures import UploadFile as StarletteUploadFile

from app.crud.book import delete_book, fetch_book, list_books, save_book, update_book
from app.dependencies.core import DBSessionDep
from app.helper.book_file import get_basename, is_file_exists, save_file
from app.models import Book as BookDBModel
from app.schemas.requests import BookCreate, BookFilter, BookUpdate
from app.schemas.responses import BookResponse

router = APIRouter(
    prefix="/api/books",
    tags=["books"],
    responses={404: {"description": "Not found"}},
)


@router.get("/{book_id}", response_model=BookResponse)
async def get_book(
    book_id: int,
    db_session: DBSessionDep,
) -> BookDBModel:
    return await fetch_book(db_session, book_id)


@router.get("", response_model=list[BookResponse])
async def get_books(
    filters: Annotated[BookFilter, Depends()], db_session: DBSessionDep
) -> Sequence[BookDBModel]:
    return await list_books(db_session, filters)


@router.post("", response_model=BookResponse)
async def create_book(
    book_data: Annotated[BookCreate, Depends(BookCreate.as_form)],
    db_session: DBSessionDep,
    file: UploadFile = File(...),
) -> BookDBModel:
    file_path = save_file(file)
    new_book = await save_book(db_session, book_data, file_path)
    return new_book


@router.put("/{book_id}", response_model=BookResponse)
async def update_book_data(
    book_id: int,
    book_data: Annotated[BookUpdate, Depends(BookUpdate.as_form)],
    db_session: DBSessionDep,
    file: UploadFile | str | None = File(None),
) -> BookDBModel:
    if isinstance(file, StarletteUploadFile) and file.filename != "":
        file_path = save_file(file)
    else:
        file_path = None  # No file uploaded
    return await update_book(db_session, book_id, book_data, file_path)


@router.get("/{book_id}/download")
async def download_book_file(
    book_id: int,
    db_session: DBSessionDep,
) -> FileResponse:
    book = await fetch_book(db_session, book_id)

    if not is_file_exists(book.file_path):
        raise HTTPException(status_code=404, detail="File not found")

    return FileResponse(
        path=book.file_path,
        filename=get_basename(book.file_path),
        media_type="application/octet-stream",
    )


@router.get("/{book_id}/preview")
async def preview_book_file(
    book_id: int,
    db_session: DBSessionDep,
) -> FileResponse:
    book = await fetch_book(db_session, book_id)

    if not is_file_exists(book.file_path):
        raise HTTPException(status_code=404, detail="File not found")

    return FileResponse(path=book.file_path, media_type="application/pdf")


@router.delete("/{book_id}", status_code=204)
async def delete_book_data(book_id: int, db_session: DBSessionDep) -> None:
    await delete_book(db_session, book_id)
