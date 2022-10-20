from abc import abstractmethod, ABC
from datetime import datetime
from typing import List, Optional
import logging

import db
import es
import helpers
from settings import Settings
from state import State
from es_models import ElasticMovie, ElasticGenre, ElasticMovieGenre, ElasticPerson, ElasticMoviePerson


class Loader(ABC):
    """Абстрактный класс загрузчика фильмов из Postgres в Elastic.

    Attributes
    ----------
    _entity : str
        Сущность, по которой ищем фильмы (film_work, genre, person).
    _state : State
        Объект состояния загрузчика.
    """
    name: str

    def __init__(self,
                 state: State,
                 settings: Settings,
                 logger: logging.Logger):
        self._entity = None
        self._pg_conn = None
        self._state = state
        self._settings = settings
        self._logger = logger

    def _prepare_es_person(self, person: dict) -> ElasticMoviePerson:
        return ElasticMoviePerson(id=person['person_id'], full_name=person['person_name'])

    def _prepare_es_genre(self, genre: dict) -> ElasticMovieGenre:
        return ElasticMovieGenre(id=genre['genre_id'], name=genre['genre_name'])

    def _prepare_es_movies(self, bulk: List[dict]) -> List[ElasticMovie]:
        """
        Трансформировать строки из Postgres в датаклассы для Elastic.
        """
        elastic_movies = []

        for row in bulk:
            actors = []
            writers = []
            directors = []

            for person in row['persons']:
                es_person = self._prepare_es_person(person)
                if person['person_role'] == 'actor':
                    actors.append(es_person)
                elif person['person_role'] == 'writer':
                    writers.append(es_person)
                elif person['person_role'] == 'director':
                    directors.append(es_person)
                else:
                    raise Exception(f'Incorrect person role ({person.role})')

            genres = [self._prepare_es_genre(g) for g in row['genres']]

            elastic_movies.append(ElasticMovie(id=row['id'],
                                               imdb_rating=row['rating'],
                                               genre_names=[g.name for g in genres],
                                               genres=genres,
                                               title=row['title'],
                                               description=row['description'],
                                               director_names=[p.full_name for p in directors],
                                               actors_names=[p.full_name for p in actors],
                                               writers_names=[p.full_name for p in writers],
                                               directors=directors,
                                               actors=actors,
                                               writers=writers))

        return elastic_movies

    def load(self) -> None:
        """
        Выполнить загрузку свежих фильмов из Postgres в Elastic.
        """
        with db.pg_connect(self._settings.PG_DSN) as self._pg_conn:
            modified_film_works = self._get_modified_film_works()

            bulk = []
            total_found = total_updated = 0
            for _bulk in modified_film_works:
                bulk = _bulk
                total_found += len(bulk)
                es_movies_bulk = self._prepare_es_movies(bulk)

                es.bulk_upsert_movies(es_movies_bulk)
                self._save_state_after_bulk(bulk)
                total_updated += len(bulk)

            if bulk:
                self._save_state_after_bulk(bulk, is_final_bulk=True)

            self._logger.info(f'Found rows: {total_found}. Updated: {total_updated}.')

    @abstractmethod
    def _get_modified_film_works(self):
        """
        Вернуть список фильмов для загрузки.
        """
        pass

    @abstractmethod
    def _save_state_after_bulk(self, bulk: List[dict], is_final_bulk: bool = False) -> None:
        """
        Сохранить состояние после успешной обработки пачки фильмов.
        """
        pass

    def _get_state(self) -> dict:
        """
        Вернуть текущее состояние загрузчика.
        """
        state = self._state.get_state(self._entity)
        if state is not None:
            return state
        return {}

    def _set_state(self, state: dict) -> None:
        """
        Обновить текущее состояние загрузчика.
        """
        self._state.set_state(self._entity, state)

    def _get_date_from_state(self, key: str) -> Optional[datetime]:
        """
        Получить значение состояния по ключу key, обернув его в datetime.
        """
        val = self._get_state().get(key)
        if val:
            return datetime.fromisoformat(val)
        return None


class OnFilmWorkUpdatedLoader(Loader):
    """
    Загрузчик фильмов, которые изменились с момента предыдущей загрузки.
    """
    def __init__(self, state: State, settings: Settings, logger: logging.Logger):
        super().__init__(state, settings, logger)
        self._entity = 'film_work'

    def _get_modified_film_works(self):
        return helpers.Query(conn=self._pg_conn) \
            .by_film_work(self._get_date_from_state('fw_last_updated')) \
            .execute()

    def _save_state_after_bulk(self, bulk: List[dict], is_final_bulk: bool = False) -> None:
        fw_last_updated = bulk[-1]['updated_at']
        self._set_state({'fw_last_updated': fw_last_updated.isoformat()})


class OnGenreUpdatedLoader(Loader):
    """
    Загрузчик фильмов, у которых изменился жанр(ы) с момента предыдущей загрузки.
    """
    def __init__(self, state: State, settings: Settings, logger: logging.Logger):
        super().__init__(state, settings, logger)
        self._entity = 'genre'

    def _get_modified_film_works(self):
        return helpers.Query(conn=self._pg_conn) \
            .by_genres(self._get_date_from_state('genre_last_updated'),
                       self._get_date_from_state('fw_last_created')) \
            .execute()

    def _save_state_after_bulk(self, bulk: List[dict], is_final_bulk: bool = False) -> None:
        genre_last_updated = bulk[-1]['min_genre_updated_at']
        fw_last_created = bulk[-1]['created_at']
        state = {
            'genre_last_updated': genre_last_updated.isoformat()
        }
        if not is_final_bulk:
            state['fw_last_created'] = fw_last_created.isoformat()

        self._set_state(state)


class OnPersonUpdatedLoader(Loader):
    """
    Загрузчик фильмов, у которых изменился участник(и) с момента предыдущей загрузки.
    """
    def __init__(self, state: State, settings: Settings, logger: logging.Logger):
        super().__init__(state, settings, logger)
        self._entity = 'person'

    def _get_modified_film_works(self):
        return helpers.Query(conn=self._pg_conn) \
            .by_persons(self._get_date_from_state('person_last_updated'),
                        self._get_date_from_state('fw_last_created')) \
            .execute()

    def _save_state_after_bulk(self, bulk: List[dict], is_final_bulk: bool = False) -> None:
        person_last_updated = bulk[-1]['min_person_updated_at']
        fw_last_created = bulk[-1]['created_at']
        state = {
            'person_last_updated': person_last_updated.isoformat()
        }
        if not is_final_bulk:
            state['fw_last_created'] = fw_last_created.isoformat()

        self._set_state(state)


class LoaderGenres(ABC):
    """Абстрактный класс загрузчика жанров из Postgres в Elastic.

    Attributes
    ----------
    _entity : str
        Сущность, по которой ищем фильмы (film_work, genre, person).
    _state : State
        Объект состояния загрузчика.
    """
    name: str

    def __init__(self,
                 state: State,
                 settings: Settings,
                 logger: logging.Logger):
        self._entity = None
        self._pg_conn = None
        self._state = state
        self._settings = settings
        self._logger = logger

    def _prepare_es_genres(self, bulk: List[dict]) -> List[ElasticGenre]:
        """
        Трансформировать строки из Postgres в датаклассы для Elastic.
        """
        elastic_entities = []

        for row in bulk:
            elastic_entities.append(ElasticGenre(
                id=row['id'],
                name=row['name'],
                description=row['description']
            )
            )

        return elastic_entities

    def load(self) -> None:
        """
        Выполнить загрузку свежих фильмов из Postgres в Elastic.
        """
        with db.pg_connect(self._settings.PG_DSN) as self._pg_conn:
            modified_entities = self._get_modified_entities('genres')

            bulk = []
            total_found = total_updated = 0
            for _bulk in modified_entities:
                bulk = _bulk
                total_found += len(bulk)
                es_entities_bulk = self._prepare_es_genres(bulk)

                es.bulk_upsert_genres(es_entities_bulk)
                self._save_state_after_bulk(bulk)
                total_updated += len(bulk)

            if bulk:
                self._save_state_after_bulk(bulk, is_final_bulk=True)

            self._logger.info(f'Found rows: {total_found}. Updated: {total_updated}.')

    @abstractmethod
    def _get_modified_entities(self):
        """
        Вернуть список фильмов для загрузки.
        """
        pass

    @abstractmethod
    def _save_state_after_bulk(self, bulk: List[dict], is_final_bulk: bool = False) -> None:
        """
        Сохранить состояние после успешной обработки пачки фильмов.
        """
        pass

    def _get_state(self) -> dict:
        """
        Вернуть текущее состояние загрузчика.
        """
        state = self._state.get_state(self._entity)
        if state is not None:
            return state
        return {}

    def _set_state(self, state: dict) -> None:
        """
        Обновить текущее состояние загрузчика.
        """
        self._state.set_state(self._entity, state)

    def _get_date_from_state(self, key: str) -> Optional[datetime]:
        """
        Получить значение состояния по ключу key, обернув его в datetime.
        """
        val = self._get_state().get(key)
        if val:
            return datetime.fromisoformat(val)
        return None


class LoaderPersons(ABC):
    """Абстрактный класс загрузчика участников из Postgres в Elastic.

    Attributes
    ----------
    _entity : str
        Сущность, по которой ищем фильмы (film_work, genre, person).
    _state : State
        Объект состояния загрузчика.
    """
    name: str

    def __init__(self,
                 state: State,
                 settings: Settings,
                 logger: logging.Logger):
        self._entity = None
        self._pg_conn = None
        self._state = state
        self._settings = settings
        self._logger = logger

    def _prepare_es_persons(self, bulk: List[dict]) -> List[ElasticPerson]:
        """
        Трансформировать строки из Postgres в датаклассы для Elastic.
        """
        elastic_entities = []

        for row in bulk:
            elastic_entities.append(ElasticPerson(
                id=row['id'],
                full_name=row['full_name']
            )
            )

        return elastic_entities

    def load(self) -> None:
        """
        Выполнить загрузку свежих фильмов из Postgres в Elastic.
        """
        with db.pg_connect(self._settings.PG_DSN) as self._pg_conn:
            modified_entities = self._get_modified_entities('persons')

            bulk = []
            total_found = total_updated = 0
            for _bulk in modified_entities:
                bulk = _bulk
                total_found += len(bulk)
                es_entities_bulk = self._prepare_es_persons(bulk)

                es.bulk_upsert_persons(es_entities_bulk)
                self._save_state_after_bulk(bulk)
                total_updated += len(bulk)

            if bulk:
                self._save_state_after_bulk(bulk, is_final_bulk=True)

            self._logger.info(f'Found rows: {total_found}. Updated: {total_updated}.')

    @abstractmethod
    def _get_modified_entities(self):
        """
        Вернуть список фильмов для загрузки.
        """
        pass

    @abstractmethod
    def _save_state_after_bulk(self, bulk: List[dict], is_final_bulk: bool = False) -> None:
        """
        Сохранить состояние после успешной обработки пачки фильмов.
        """
        pass

    def _get_state(self) -> dict:
        """
        Вернуть текущее состояние загрузчика.
        """
        state = self._state.get_state(self._entity)
        if state is not None:
            return state
        return {}

    def _set_state(self, state: dict) -> None:
        """
        Обновить текущее состояние загрузчика.
        """
        self._state.set_state(self._entity, state)

    def _get_date_from_state(self, key: str) -> Optional[datetime]:
        """
        Получить значение состояния по ключу key, обернув его в datetime.
        """
        val = self._get_state().get(key)
        if val:
            return datetime.fromisoformat(val)
        return None


class OnGenresUpdatedLoader(LoaderGenres):
    """
    Загрузчик жанров, которые изменились с момента предыдущей загрузки.
    """
    def __init__(self, state: State, settings: Settings, logger: logging.Logger):
        super().__init__(state, settings, logger)
        self._entity = 'genres'
        self._sql_text = "select id, name, description, updated_at from content.genre where updated_at > '{updated_at}' order by updated_at"

    def _get_modified_entities(self, entity: str):
        return helpers.QueryEntity(
            conn=self._pg_conn,
            sql_text=self._sql_text,
            entity_updated_after=self._get_date_from_state(entity + '_last_updated')
        ).execute()

    def _save_state_after_bulk(self, bulk: List[dict], is_final_bulk: bool = False) -> None:
        entity_last_updated = bulk[-1]['updated_at']
        state = {
            self._entity + '_last_updated': entity_last_updated.isoformat()
        }

        self._set_state(state)


class OnPersonsUpdatedLoader(LoaderPersons):
    """
    Загрузчик участников, которые изменились с момента предыдущей загрузки.
    """
    def __init__(self, state: State, settings: Settings, logger: logging.Logger):
        super().__init__(state, settings, logger)
        self._entity = 'persons'
        self._sql_text = "select id, full_name, updated_at from content.person where updated_at > '{updated_at}' order by updated_at"

    def _get_modified_entities(self, entity: str):
        return helpers.QueryEntity(
            conn=self._pg_conn,
            sql_text=self._sql_text,
            entity_updated_after=self._get_date_from_state(entity + '_last_updated')
        ).execute()

    def _save_state_after_bulk(self, bulk: List[dict], is_final_bulk: bool = False) -> None:
        entity_last_updated = bulk[-1]['updated_at']
        state = {
            self._entity + '_last_updated': entity_last_updated.isoformat()
        }

        self._set_state(state)


def create_loader_for_entity(entity: str, state: State, settings: Settings, logger: logging.Logger):
    """
    Создать загрузчик для сущности entity.
    """
    loaders = {
        'film_work': OnFilmWorkUpdatedLoader,
        'genre': OnGenreUpdatedLoader,
        'person': OnPersonUpdatedLoader,
        'genres': OnGenresUpdatedLoader,
        'persons': OnPersonsUpdatedLoader
    }
    loader_cls = loaders.get(entity)
    if loader_cls is None:
        raise Exception(f'Undefined loader entity ({entity})')

    return loader_cls(state, settings, logger)
