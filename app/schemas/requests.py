from datetime import date
from typing import Annotated, Any

from fastapi import Form, Query
from fastapi.exceptions import RequestValidationError
from pydantic import BaseModel, field_validator


class BookFilter(BaseModel):
    name: str | None = None
    author: str | None = None
    genre: str | None = None
    date_published: date | None = None
    limit: Annotated[int, Query(ge=1, le=100)] = 100
    offset: Annotated[int, Query(ge=0)] = 0


class BookCreate(BaseModel):
    name: str
    author: str
    genre: str
    date_published: date

    @classmethod
    def as_form(
        cls,
        name: Annotated[str, Form()],
        author: Annotated[str, Form()],
        genre: Annotated[str, Form()],
        date_published: Annotated[date, Form()],
    ) -> BaseModel:
        return cls(
            name=name,
            author=author,
            genre=genre,
            date_published=date_published,
        )


class BookUpdate(BaseModel):
    name: str | None = None
    author: str | None = None
    genre: str | None = None
    date_published: date | None = None

    @field_validator("date_published", mode="before")
    @classmethod
    def parse_date(cls, v: Any) -> Any:
        if v in (None, ""):
            return None
        try:
            return v
        except ValueError:
            raise RequestValidationError(
                "date_published must be in format YYYY-MM-DD",
            )

    @classmethod
    def as_form(
        cls,
        name: str | None = Form(None),
        author: str | None = Form(None),
        genre: str | None = Form(None),
        date_published: date | None = Form(None),
    ) -> BaseModel:
        return cls(
            name=name,
            author=author,
            genre=genre,
            date_published=date_published,
        )
