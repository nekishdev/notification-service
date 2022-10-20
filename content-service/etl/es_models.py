from typing import List, Optional
from uuid import UUID
from dataclasses import dataclass


@dataclass()
class ElasticMoviePerson:
    id: UUID
    full_name: str


@dataclass()
class ElasticMovieGenre:
    id: UUID
    name: str


@dataclass()
class ElasticMovie:
    id: UUID
    imdb_rating: float

    genre_names: List[str]
    genres: List[ElasticMovieGenre]

    title: str
    description: Optional[str]

    director_names: List[str]
    actors_names: List[str]
    writers_names: List[str]

    directors: List[ElasticMoviePerson]
    actors: List[ElasticMoviePerson]
    writers: List[ElasticMoviePerson]


@dataclass()
class ElasticGenre:
    id: UUID
    name: str
    description: str


@dataclass()
class ElasticPerson:
    id: UUID
    full_name: str
