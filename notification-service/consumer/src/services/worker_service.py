from contextlib import contextmanager

import psycopg2
from models.notifications import Message
from services.postgres_saver import PostgresSaver
from psycopg2.extras import DictCursor
from settings import dsl, pg_settings


@contextmanager
def pg_conn_context(dsl_: dict):
    conn = psycopg2.connect(**dsl_, cursor_factory=DictCursor)
    yield conn
    conn.close()


def save_message(msg: Message):
    try:
        with pg_conn_context(dsl) as pg_conn:
            postgres_saver = PostgresSaver(pg_conn)
            postgres_saver.insert_message(msg)
    except Exception:
        raise


def set_message_status(msg: Message):
    try:
        with pg_conn_context(dsl) as pg_conn:
            postgres_saver = PostgresSaver(pg_conn)
            postgres_saver.update_message(msg)
    except Exception:
        raise
