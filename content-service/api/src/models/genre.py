from typing import Optional

from models.base import BaseOrjsonModel
from pydantic import constr


class Genre(BaseOrjsonModel):
    id: str
    name: constr(max_length=255, min_length=1)
    description: Optional[str]
