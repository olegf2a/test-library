from datetime import datetime

from pydantic import BaseModel, ConfigDict


class Book(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: int
    name: str
    author: str
    genre: str
    date_published: datetime
