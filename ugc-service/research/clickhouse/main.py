from typing import Any, Dict, Generator, Tuple

import time
from functools import wraps
from random import randint

from clickhouse_driver import Client


def timeit(func):
    @wraps(func)
    def timeit_wrapper(*args, **kwargs):
        start_time = time.perf_counter()
        func_result = func(*args, **kwargs)
        end_time = time.perf_counter()
        total_time = end_time - start_time
        print(f'Function {func.__name__} {kwargs} Took {total_time:.4f} seconds')
        return func_result

    return timeit_wrapper


def rows_generator(count: int) -> Generator[Dict[str, int], Any, None]:
    for _ in range(count):
        yield {
            'user_id': randint(0, 100),
            'movie_id': randint(0, 100),
            'viewed_frame': randint(0, 100),
        }


def batch_generator(size: int, count: int) -> Generator[Tuple[Tuple[int, ...], ...], Any, None]:
    for _ in range(count):
        yield tuple(tuple(row.values()) for row in rows_generator(size))


@timeit
def test_select(_cursor: Client, *, sql: str) -> None:
    _cursor.execute(sql)


@timeit
def insert_to_clickhouse(client: Client, size: int, count: int) -> None:
    for batch in batch_generator(count, size):
        client.execute('INSERT INTO example.regular_table2 (user_id, movie_id, viewed_frame) VALUES',
                       batch,
                       types_check=True)


if __name__ == '__main__':
    cursor = Client(host='localhost')

    cursor.execute('CREATE DATABASE IF NOT EXISTS example ON CLUSTER company_cluster')
    cursor.execute(
        'CREATE TABLE IF NOT EXISTS example.regular_table2 ON CLUSTER company_cluster'
        ' (id UInt32,user_id UInt32, movie_id UInt32, viewed_frame UInt32) Engine=MergeTree()  ORDER BY id')

    insert_to_clickhouse(cursor, size=1_000, count=1)
    insert_to_clickhouse(cursor, size=10_000, count=1)
    insert_to_clickhouse(cursor, size=100_000, count=1)
    insert_to_clickhouse(cursor, size=1_000_000, count=1)

    test_select(cursor, sql='select count(*) from example.regular_table2')
    test_select(cursor,
                sql='select count(*) from example.regular_table2  where viewed_frame between 2000000 and 3000000')
    test_select(cursor, sql='SELECT max(viewed_frame), user_id FROM example.regular_table2 group by user_id')
    test_select(cursor, sql='SELECT count(DISTINCT user_id) FROM example.regular_table2')
    print(cursor.execute('select count(*) from example.regular_table2 '))
