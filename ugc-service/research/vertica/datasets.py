from typing import Any, Dict, Generator, List, Tuple, Union

from random import randint


def rows_generator(count: int) -> Generator[Dict[str, Union[int, str]], Any, None]:
    user_id = randint(100_000, 999_999)
    movie_id = 'tt_' + str(randint(10_000, 99_999))
    viewed_frame = randint(1_000_000, 3_000_000)
    for _ in range(count):
        yield {
            'user_id': user_id,
            'movie_id': movie_id,
            'viewed_frame': viewed_frame
        }


def batch_generator(size: int, count: int) -> Generator[List[Tuple[Any, ...]], Any, None]:
    for _ in range(count):
        yield [tuple(row.values()) for row in rows_generator(size)]
