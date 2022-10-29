from contextlib import contextmanager

import psycopg2
from psycopg2 import DatabaseError as PostgresDatabaseError
from psycopg2.extensions import connection as _connection
from psycopg2.extras import DictCursor

from postgres_saver import PostgresSaver
from settings import pg_settings, dsl
from models.notifications import Message
from datetime import datetime as datetime_, timezone
from uuid import uuid4


@contextmanager
def pg_conn_context(dsl_: dict):
    conn = psycopg2.connect(**dsl_, cursor_factory=DictCursor)
    yield conn
    conn.close()


def save_message(msg: Message):
    try:
        print(dsl)
        with pg_conn_context(dsl) as pg_conn:
            postgres_saver = PostgresSaver(pg_conn)

            print(postgres_saver)
            print(msg)
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


def load_from_notify_db(pg_conn_: _connection) -> None:
    postgres_saver = PostgresSaver(pg_conn_)

    dt = datetime_.now(timezone.utc)
    try:
        msg = Message(
            id=uuid4(),
            created=dt,
            modified=dt,
            address='nowar1@mail.ru',
            source='email',
            subject='subject',
            text='text',
            send_at=dt,
            status='processing'
        )

        postgres_saver.insert_message(msg)

    except (Exception, PostgresDatabaseError) as error:
        # app_logger.error('Saver: {message}'.format(message=error))
        print(str(error))
        return


if __name__ == '__main__':

    # DSL = pg_settings.PG_DSN
    print(dsl)
    try:
        with pg_conn_context(dsl) as pg_conn:
            load_from_notify_db(pg_conn)

    except Exception:
        raise
