import uuid

from models.base import BaseOrjsonModel


class Person(BaseOrjsonModel):
    id: uuid.UUID
    full_name: str
