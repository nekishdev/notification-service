import typing as t
import uuid

from elasticsearch import AsyncElasticsearch, NotFoundError

from models.film import Film
from repositories.film import FilmRepository


class ElasticFilmRepository(FilmRepository):
    """
    Хранилище фильмов в Elasticsearch.
    """

    def __init__(self, elastic: AsyncElasticsearch, index: str):
        self._elastic: AsyncElasticsearch = elastic
        self._index: str = index
        self._model = Film

    async def get_by_id(self, doc_id: uuid.UUID):
        try:
            doc = await self._elastic.get(self._index, doc_id)
        except NotFoundError:
            return None
        return self._model(**doc['_source'])

    async def filter(
        self,
        *,
        sort: t.Optional[str] = None,
        page_size: t.Optional[int] = None,
        page_number: t.Optional[int] = None,
        search_phrase: t.Optional[str] = None,
        genre_id: t.Optional[uuid.UUID] = None,
        person_id: t.Optional[uuid.UUID] = None,
    ) -> t.List[Film]:
        try:
            if sort and sort.startswith('-'):
                sort_field = sort[1:]
                sort_direction = 'desc'
            else:
                sort_field = sort
                sort_direction = 'asc'

            body = {}

            if page_size is not None and page_number is not None:
                body['from'] = self._get_offset(page_number, page_size)
                body['size'] = page_size

            if sort_field:
                body['sort'] = [{sort_field: sort_direction}]

            query: dict = {'bool': {}}

            must_clause: list = []

            if search_phrase:
                must_clause.append(
                    {
                        'multi_match': {
                            'query': search_phrase,
                            'fields': [
                                'title',
                                'description',
                                'actors_names',
                                'directors_names',
                                'writers_names',
                                'genres_names',
                            ],
                        }
                    }
                )

            if genre_id:
                must_clause.append(self._prepare_nested_clause('genres', 'id', str(genre_id)))

            if person_id:
                query['bool']['should'] = [
                    self._prepare_nested_clause('directors', 'id', str(person_id)),
                    self._prepare_nested_clause('writers', 'id', str(person_id)),
                    self._prepare_nested_clause('actors', 'id', str(person_id)),
                ]

            if must_clause:
                query['bool']['must'] = must_clause

            body['query'] = query

            response = await self._elastic.search(index=self._index, body=body)
            docs = response['hits']['hits']
        except NotFoundError:
            return []
        return [self._model(**doc['_source']) for doc in docs]

    def _get_offset(self, page_number: int, page_size: int) -> int:
        return page_size * (page_number - 1)

    def _prepare_nested_clause(self, path: str, field: str, val: str) -> dict:
        return {
            'nested': {
                'path': path,
                'query': {'bool': {'must': [{'match': {f'{path}.{field}': val}}]}},
                'score_mode': 'avg',
            }
        }
