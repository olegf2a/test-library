from datetime import date

from sqlalchemy import BigInteger, Date, String
from sqlalchemy.orm import Mapped, mapped_column

from . import Base


class Book(Base):
    __tablename__ = "book"

    id: Mapped[int] = mapped_column(
        BigInteger,
        primary_key=True,
    )
    name: Mapped[str] = mapped_column(
        String(256),
        nullable=False,
        index=True,
    )
    author: Mapped[str] = mapped_column(
        String(256),
        nullable=False,
        index=True,
    )
    genre: Mapped[str] = mapped_column(
        String(256),
        nullable=False,
        index=True,
    )
    date_published: Mapped[date] = mapped_column(
        Date(),
        nullable=False,
    )
    file_path: Mapped[str] = mapped_column(
        String,
        nullable=True,
    )
