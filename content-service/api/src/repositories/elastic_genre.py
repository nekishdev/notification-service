import typing as t
import uuid

from elasticsearch import AsyncElasticsearch, NotFoundError, RequestError

from models.genre import Genre
from repositories.genre import GenreRepository


class ElasticGenreRepository(GenreRepository):
    """
    Хранилище жанров в Elasticsearch.
    """

    def __init__(self, elastic: AsyncElasticsearch, index: str):
        self._elastic: AsyncElasticsearch = elastic
        self._index: str = index
        self._model = Genre

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
        search_phrase: t.Optional[str] = None
    ) -> t.List[Genre]:
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
                        'match': {
                            'name': {
                                'query': search_phrase,
                                'fuzziness': 'AUTO',
                                'operator': 'and',
                            }
                        }
                    }
                )

            if must_clause:
                query['bool']['must'] = must_clause

            body['query'] = query

            response = await self._elastic.search(index=self._index, body=body)
            docs = response['hits']['hits']
        except RequestError as error:
            return [], error
        except NotFoundError:
            return [], None
        return [self._model(**doc['_source']) for doc in docs], None

    async def all(self) -> t.List[Genre]:
        try:
            response = await self._elastic.search(index=self._index, size=1000)
            docs = response['hits']['hits']
        except NotFoundError:
            return []
        return [self._model(**doc['_source']) for doc in docs]

    def _get_offset(self, page_number: int, page_size: int) -> int:
        return page_size * (page_number - 1)
