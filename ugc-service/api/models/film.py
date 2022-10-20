import datetime
import uuid

import pydantic as pd
from pydantic import Field


class Film(pd.BaseModel):
    id: uuid.UUID = Field(alias="_id")
    like_count: int = Field(default=0)
    dislike_count: int = Field(default=0)
    score_count: int = Field(default=0)
    avg_score: float = Field(default=0)


class FilmScore(pd.BaseModel):
    film_id: uuid.UUID
    user_id: uuid.UUID
    score_value: int
    date_create: datetime.datetime = Field(default_factory=datetime.datetime.now)

    # TODO: refactor: add validator for value
