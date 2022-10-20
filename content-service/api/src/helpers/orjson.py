from typing import List

import orjson
from pydantic import BaseModel


def default(obj):
    return obj.__dict__


def orjson_dumps(v, *, default):
    return orjson.dumps(v, default=default).decode()


def dumps_model_list(models: List[BaseModel]) -> str:
    dml = [model.dict() for model in models]

    return orjson_dumps(dml, default=default)
