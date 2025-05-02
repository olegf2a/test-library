from collections.abc import Sequence

from fastapi import HTTPException
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.sql.elements import ColumnElement

from app.helper.book_file import remove_file
from app.models import Book as BookDBModel
from app.schemas.requests import BookCreate, BookFilter, BookUpdate


async def fetch_book(db_session: AsyncSession, book_id: int) -> BookDBModel:
    stmt = select(BookDBModel).where(BookDBModel.id == book_id)
    book = (await db_session.scalars(stmt)).first()
    if not book:
        raise HTTPException(status_code=404, detail="Book not found")
    return book


async def list_books(
    db_session: AsyncSession, filters: BookFilter
) -> Sequence[BookDBModel]:
    conditions: list[ColumnElement[bool]] = []
    if filters.name:
        conditions.append(BookDBModel.name.ilike(f"%{filters.name}%"))
    if filters.author:
        conditions.append(BookDBModel.author.ilike(f"%{filters.author}%"))
    if filters.genre:
        conditions.append(BookDBModel.genre.ilike(f"%{filters.genre}%"))
    if filters.genre:
        conditions.append(
            BookDBModel.date_published == filters.date_published,
        )

    stmt = select(BookDBModel)
    if conditions:
        stmt = stmt.where(*conditions)
    stmt = stmt.limit(filters.limit).offset(filters.limit * filters.offset)

    books = (await db_session.scalars(stmt)).all()
    if not books:
        raise HTTPException(status_code=404, detail="Book(s) not found")
    return books


async def save_book(
    db_session: AsyncSession, book_data: BookCreate, file_path: str
) -> BookDBModel:
    new_book = BookDBModel(
        name=book_data.name,
        author=book_data.author,
        genre=book_data.genre,
        date_published=book_data.date_published,
        file_path=file_path,
    )
    db_session.add(new_book)
    await db_session.commit()
    await db_session.refresh(new_book)
    return new_book


async def update_book(
    db_session: AsyncSession,
    book_id: int,
    book_data: BookUpdate,
    file_path: str | None = None,
) -> BookDBModel:
    book = await fetch_book(db_session, book_id)
    data_to_update = filter(
        lambda kv: kv[1] not in (None, ""),
        book_data.model_dump(exclude_unset=True).items(),
    )
    old_file = None

    for field, value in dict(data_to_update).items():
        setattr(book, field, value)

    if file_path and book.file_path != file_path:
        old_file = book.file_path
        book.file_path = file_path

    await db_session.commit()
    await db_session.refresh(book)
    if old_file:
        remove_file(old_file)
    return book


async def delete_book(db_session: AsyncSession, book_id: int) -> None:
    book = await fetch_book(db_session, book_id)
    await db_session.delete(book)
    await db_session.commit()
    remove_file(book.file_path)
