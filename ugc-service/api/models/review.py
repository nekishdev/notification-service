import datetime
import uuid

import pydantic as pd
from pydantic import Field

import models.enums as enums


class ReviewScore(pd.BaseModel):
    user_id: uuid.UUID
    score_value: enums.ScoreValueEnum
    date_create: datetime.datetime = Field(default_factory=datetime.datetime.now)


class Review(pd.BaseModel):
    id: uuid.UUID = Field(alias="_id", default_factory=uuid.uuid4)
    user_id: uuid.UUID
    film_id: uuid.UUID
    text: str
    date_create: datetime.datetime = Field(default_factory=datetime.datetime.now)
    scores: list[ReviewScore]
