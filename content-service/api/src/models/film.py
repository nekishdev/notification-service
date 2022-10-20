import uuid
from typing import Optional, List

from models.base import BaseOrjsonModel
from models.genre import Genre
from models.person import Person


class Film(BaseOrjsonModel):
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
