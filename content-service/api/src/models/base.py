import orjson
from pydantic import BaseModel

from helpers.orjson import orjson_dumps


class BaseOrjsonModel(BaseModel):
    class Config:
        json_loads = orjson.loads
        json_dumps = orjson_dumps
