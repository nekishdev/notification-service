from enum import Enum


class ScoreValueEnum(int, Enum):
    LIKE: int = 10
    DISLIKE: int = 0
