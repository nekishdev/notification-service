import vertica_python
from vertica_python.vertica.connection import Cursor

from research.vertica.datasets import batch_generator, rows_generator
from research.vertica.helpers import timeit

connection_info = {
    'host': '127.0.0.1',
    'port': 15433,
    'user': 'dbadmin',
    'password': '',
    'database': 'docker',
    'autocommit': True,
}


@timeit
def test_single_insert(_cursor: Cursor, *, count: int) -> None:
    for row in rows_generator(count):
        _cursor.execute(f"""
        INSERT INTO views (user_id, movie_id, viewed_frame) VALUES ({row['user_id']}, '{row['movie_id']}', {row['viewed_frame']})
        """)


@timeit
def test_batch_insert(_cursor: Cursor, *, size: int, count: int) -> None:
    for batch in batch_generator(size, count):
        _cursor.executemany("""
        INSERT INTO views (user_id, movie_id, viewed_frame) VALUES (%s, %s, %s)
        """, batch)


@timeit
def test_select(_cursor: Cursor, *, sql: str) -> None:
    _cursor.execute(sql)


with vertica_python.connect(**connection_info) as connection:
    cursor = connection.cursor()
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS views (
        id IDENTITY,
        user_id INTEGER NOT NULL,
        movie_id VARCHAR(256) NOT NULL,
        viewed_frame INTEGER NOT NULL
    );
    """)

    cnt = cursor.execute('select count(*) from views').fetchone()
    print('cnt = ', cnt)

    test_single_insert(cursor, count=100)
    test_single_insert(cursor, count=1000)

    test_batch_insert(cursor, size=1_000, count=1)
    test_batch_insert(cursor, size=10_000, count=1)
    test_batch_insert(cursor, size=100_000, count=1)
    test_batch_insert(cursor, size=1_000_000, count=1)

    test_select(cursor, sql='select count(*) from views')
    test_select(cursor, sql='select count(*) from views where viewed_frame between 2000000 and 3000000')
    test_select(cursor, sql='SELECT max(viewed_frame), user_id FROM views group by user_id')
    test_select(cursor, sql='SELECT count(DISTINCT user_id) FROM views')
