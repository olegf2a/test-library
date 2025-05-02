from datetime import datetime

from pydantic import BaseModel


class BookResponse(BaseModel):
    model_config = {"from_attributes": True}

    id: int
    name: str
    author: str
    genre: str
    date_published: datetime
