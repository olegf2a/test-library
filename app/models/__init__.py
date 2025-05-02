# need access to this before importing models
from app.core.database import Base

from .book import Book

__all__ = ["Base", "Book"]
