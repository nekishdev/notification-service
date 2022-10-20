"""
Модуль для хранения настроек подключения к БД.
"""
from typing import Union

import backoff
import psycopg2
from psycopg2.extras import DictCursor
from contextlib import contextmanager


@contextmanager
def pg_connect(dsn: Union[dict, str]):
    """
    Возвращает соединение с БД Postgres. Гарантирует закрытие соединения.
    """
    @backoff.on_exception(backoff.expo,
                          psycopg2.Error,
                          max_time=60)
    def _connect():
        return psycopg2.connect(dsn, cursor_factory=DictCursor)

    conn = _connect()
    yield conn
    conn.close()
