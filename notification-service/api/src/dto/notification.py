import typing as t
from datetime import datetime
from uuid import UUID

import pydantic as pd


class NotificationDTO(pd.BaseModel):
    id: t.Optional[UUID]
    address: str
    source: str
    text: str
    send_at: t.Optional[datetime]
