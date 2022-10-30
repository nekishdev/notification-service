from dataclasses import dataclass
from datetime import datetime as _datetime
from typing import Optional
from uuid import UUID

from email_validator import validate_email
from pydantic import BaseModel, validator


@dataclass
class Message:
    created: _datetime
    modified: _datetime
    address: str
    source: str
    subject: str
    text: str
    send_at: _datetime
    status: str
    id: Optional[UUID] = None


class NotificationSchema(BaseModel):
    id: Optional[UUID]
    address: str
    source: str
    subject: Optional[str]
    text: str
    send_at: Optional[_datetime]


class User(BaseModel):
    username: str
    user_email: str

    @validator("user_email")
    def email_validation(cls, value):
        valid_email = validate_email(value)
        return valid_email.email
