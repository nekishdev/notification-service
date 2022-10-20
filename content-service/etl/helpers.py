from datetime import datetime
from typing import Optional

import backoff
import psycopg2


class Query:
    """
    Класс для формирования SQL запроса к Postgres.
    """
    def __init__(self, conn, chunk_size: int = 100):
        self._conn = conn
        self._chunk_size = chunk_size

        self._select = [
            'fw.id',
            'fw.title',
            'fw.description',
            'fw.rating',
            'fw.type',
            'fw.created_at',
            'fw.updated_at',
            """COALESCE (
                   json_agg(
                       DISTINCT jsonb_build_object(
                           'genre_id', g.id,
                           'genre_name', g.name
                       )
                   ) FILTER (WHERE g.id is not null),
                   '[]'
               ) as genres""",
            """COALESCE (
                   json_agg(
                       DISTINCT jsonb_build_object(
                           'person_role', pfw.role,
                           'person_id', p.id,
                           'person_name', p.full_name
                       )
                   ) FILTER (WHERE p.id is not null),
                   '[]'
               ) as persons""",
        ]
        self._where = []
        self._order_by = []

    def build_sql(self) -> str:
        """
        Построить итоговый SQL запрос.
        """
        return f"""
            SELECT
               {self._select_sql()}
            FROM content.film_work fw
            LEFT JOIN content.person_film_work pfw ON pfw.film_work_id = fw.id
            LEFT JOIN content.person p ON p.id = pfw.person_id
            LEFT JOIN content.genre_film_work gfw ON gfw.film_work_id = fw.id
            LEFT JOIN content.genre g ON g.id = gfw.genre_id
            {self._where_sql()}
            GROUP BY fw.id
            {self._order_by_sql()}
        """

    @backoff.on_exception(backoff.expo,
                          psycopg2.Error,
                          max_time=60)
    def execute(self):
        """
        Выполнить запрос. Вернуть генератор, который будет отдавать строки пачками по _chunk_size.
        """
        with self._conn.cursor() as cursor:
            cursor.execute(self.build_sql())
            while True:
                data = cursor.fetchmany(self._chunk_size)
                if not data:
                    break

                yield data

    def by_film_work(self, fw_updated_after: Optional[datetime] = None):
        """
        Подготовить запрос с фильтром по дате изменения фильма.
        """
        if fw_updated_after is not None:
            self._where.append(f"fw.updated_at > '{fw_updated_after.isoformat()}'")
        self._order_by = ['fw.updated_at']

        return self

    def by_genres(self,
                  genre_updated_after: Optional[datetime] = None,
                  fw_created_after: Optional[datetime] = None):
        """Подготовить запрос для фильмов по жанрам.

        Args:
            genre_updated_after: фильмы, у которых самая ранняя дата обновления жанра
                больше переданной.
            fw_created_after: дата создания фильма больше переданной.
        """
        self._select.append('MIN(g.updated_at) as min_genre_updated_at')
        self._where.append('g.id IS NOT NULL')

        if genre_updated_after is not None:
            if fw_created_after is not None:
                self._where.append(f"g.updated_at >= '{genre_updated_after.isoformat()}'")
                self._where.append(f"fw.created_at > '{fw_created_after.isoformat()}'")
            else:
                self._where.append(f"g.updated_at > '{genre_updated_after.isoformat()}'")

        self._order_by = ['min_genre_updated_at', 'fw.created_at']

        return self

    def by_persons(self,
                   person_updated_after: Optional[datetime] = None,
                   fw_created_after: Optional[datetime] = None):
        """Подготовить запрос для фильмов по персонам.

        Args:
            person_updated_after: фильмы, у которых самая ранняя дата обновления персонажа
                больше переданной.
            fw_created_after: дата создания фильма больше переданной.
        """
        self._select.append('MIN(p.updated_at) as min_person_updated_at')
        self._where.append('p.id IS NOT NULL')

        if person_updated_after is not None:
            if fw_created_after is not None:
                self._where.append(f"p.updated_at >= '{person_updated_after.isoformat()}'")
                self._where.append(f"fw.created_at > '{fw_created_after.isoformat()}'")
            else:
                self._where.append(f"p.updated_at > '{person_updated_after.isoformat()}'")

        self._order_by = ['min_person_updated_at', 'fw.created_at']

        return self

    def _where_sql(self) -> str:
        """
        Вернуть часть SQL-запроса для WHERE.
        """
        if self._where:
            return 'WHERE ' + ' AND '.join(self._where)
        return ''

    def _order_by_sql(self) -> str:
        """
        Вернуть часть SQL-запроса для ORDER BY.
        """
        if self._order_by:
            return 'ORDER BY ' + ', '.join(self._order_by)
        return ''

    def _select_sql(self):
        """
        Вернуть часть SQL-запроса для SELECT.
        """
        return ",\n".join(self._select)


class QueryEntity:
    """
    Класс для формирования SQL запроса к Postgres.
    """
    def __init__(self, conn, sql_text: str, chunk_size: int = 100, entity_updated_after: Optional[datetime] = None):
        self._conn = conn
        self._chunk_size = chunk_size

        self._sql_text = sql_text
        if entity_updated_after is None:
            entity_updated_after = datetime.min
        self._sql_text = self._sql_text.format(updated_at=entity_updated_after.isoformat())

    def build_sql(self) -> str:
        """
        Построить итоговый SQL запрос.
        """
        return self._sql_text


    @backoff.on_exception(backoff.expo,
                          psycopg2.Error,
                          max_time=60)
    def execute(self):
        """
        Выполнить запрос. Вернуть генератор, который будет отдавать строки пачками по _chunk_size.
        """
        with self._conn.cursor() as cursor:
            cursor.execute(self.build_sql())
            while True:
                data = cursor.fetchmany(self._chunk_size)
                if not data:
                    break

                yield data


