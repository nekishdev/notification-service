import uuid
from typing import Optional, List

from pydantic import BaseModel


class Genre(BaseModel):
    id: uuid.UUID
    name: str


class Person(BaseModel):
    id: uuid.UUID
    full_name: str


class Film(BaseModel):
    id: uuid.UUID
    title: str
    description: Optional[str]
    imdb_rating: Optional[float]

    genres: List[Genre]
    genre_names: List[str]

    directors: List[Person]
    actors: List[Person]
    writers: List[Person]

    director_names: List[str]
    actors_names: List[str]
    writers_names: List[str]
