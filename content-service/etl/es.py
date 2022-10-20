import dataclasses
from typing import List

from elasticsearch import Elasticsearch, ElasticsearchException
import backoff

from es_models import ElasticGenre, ElasticMovie, ElasticPerson
from settings import settings


def _get_elasticsearch() -> Elasticsearch:
    """
    Вернуть клиент Elasticsearch.
    """
    host = settings.ELASTIC_HOST
    port = settings.ELASTIC_PORT
    return Elasticsearch([f'{host}:{port}'])


elasticsearch = _get_elasticsearch()


@backoff.on_exception(backoff.expo,
                      ElasticsearchException,
                      max_time=60)
def ensure_movies_index_exists() -> None:
    """
    Проверить, что индекс для фильмов существует. Если нет - создать.
    """
    global elasticsearch
    index = settings.ELASTIC_MOVIES_INDEX_NAME

    if not elasticsearch.indices.exists(index):
        elasticsearch.indices.create(index, {
            "settings": {
                "refresh_interval": "1s",
                "analysis": {
                    "filter": {
                        "english_stop": {
                            "type": "stop",
                            "stopwords": "_english_"
                        },
                        "english_stemmer": {
                            "type": "stemmer",
                            "language": "english"
                        },
                        "english_possessive_stemmer": {
                            "type": "stemmer",
                            "language": "possessive_english"
                        },
                        "russian_stop": {
                            "type": "stop",
                            "stopwords": "_russian_"
                        },
                        "russian_stemmer": {
                            "type": "stemmer",
                            "language": "russian"
                        }
                    },
                    "analyzer": {
                        "ru_en": {
                            "tokenizer": "standard",
                            "filter": [
                                "lowercase",
                                "english_stop",
                                "english_stemmer",
                                "english_possessive_stemmer",
                                "russian_stop",
                                "russian_stemmer"
                            ]
                        }
                    }
                }
            },
            "mappings": {
                "dynamic": "strict",
                "properties": {
                    "id": {
                        "type": "keyword"
                    },
                    "imdb_rating": {
                        "type": "float"
                    },
                    "genres": {
                        "type": "nested",
                        "dynamic": "strict",
                        "properties": {
                            "id": {
                                "type": "keyword"
                            },
                            "name": {
                                "type": "text",
                                "analyzer": "ru_en"
                            }
                        }
                    },
                    "genre_names": {
                        "type": "keyword"
                    },
                    "title": {
                        "type": "text",
                        "analyzer": "ru_en",
                        "fields": {
                            "raw": {
                                "type": "keyword"
                            }
                        }
                    },
                    "description": {
                        "type": "text",
                        "analyzer": "ru_en"
                    },
                    "director_names": {
                        "type": "text",
                        "analyzer": "ru_en"
                    },
                    "actors_names": {
                        "type": "text",
                        "analyzer": "ru_en"
                    },
                    "writers_names": {
                        "type": "text",
                        "analyzer": "ru_en"
                    },
                    "directors": {
                        "type": "nested",
                        "dynamic": "strict",
                        "properties": {
                            "id": {
                                "type": "keyword"
                            },
                            "full_name": {
                                "type": "text",
                                "analyzer": "ru_en"
                            }
                        }
                    },
                    "actors": {
                        "type": "nested",
                        "dynamic": "strict",
                        "properties": {
                            "id": {
                                "type": "keyword"
                            },
                            "full_name": {
                                "type": "text",
                                "analyzer": "ru_en"
                            }
                        }
                    },
                    "writers": {
                        "type": "nested",
                        "dynamic": "strict",
                        "properties": {
                            "id": {
                                "type": "keyword"
                            },
                            "full_name": {
                                "type": "text",
                                "analyzer": "ru_en"
                            }
                        }
                    }
                }
            }
        })


@backoff.on_exception(backoff.expo,
                      ElasticsearchException,
                      max_time=60)
def ensure_genres_index_exists() -> None:
    """
    Проверить, что индекс для жанров существует. Если нет - создать.
    """
    global elasticsearch
    index = settings.ELASTIC_GENRES_INDEX_NAME

    if not elasticsearch.indices.exists(index):
        elasticsearch.indices.create(index, {
            "settings": {
                "refresh_interval": "1s",
                "analysis": {
                    "filter": {
                        "english_stop": {
                            "type": "stop",
                            "stopwords": "_english_"
                        },
                        "english_stemmer": {
                            "type": "stemmer",
                            "language": "english"
                        },
                        "english_possessive_stemmer": {
                            "type": "stemmer",
                            "language": "possessive_english"
                        },
                        "russian_stop": {
                            "type": "stop",
                            "stopwords": "_russian_"
                        },
                        "russian_stemmer": {
                            "type": "stemmer",
                            "language": "russian"
                        }
                    },
                    "analyzer": {
                        "ru_en": {
                            "tokenizer": "standard",
                            "filter": [
                                "lowercase",
                                "english_stop",
                                "english_stemmer",
                                "english_possessive_stemmer",
                                "russian_stop",
                                "russian_stemmer"
                            ]
                        }
                    }
                }
            },
            "mappings": {
                "dynamic": "strict",
                "properties": {
                    "id": {
                        "type": "keyword"
                    },
                    "name": {
                        "type": "keyword"
                    },
                    "description": {
                        "type": "text",
                        "analyzer": "ru_en",
                    }
                }
            }
        })


@backoff.on_exception(backoff.expo,
                      ElasticsearchException,
                      max_time=60)
def ensure_persons_index_exists() -> None:
    """
    Проверить, что индекс для участников существует. Если нет - создать.
    """
    global elasticsearch
    index = settings.ELASTIC_PERSONS_INDEX_NAME

    if not elasticsearch.indices.exists(index):
        elasticsearch.indices.create(index, {
            "settings": {
                "refresh_interval": "1s",
                "analysis": {
                    "filter": {
                        "english_stop": {
                            "type": "stop",
                            "stopwords": "_english_"
                        },
                        "english_stemmer": {
                            "type": "stemmer",
                            "language": "english"
                        },
                        "english_possessive_stemmer": {
                            "type": "stemmer",
                            "language": "possessive_english"
                        },
                        "russian_stop": {
                            "type": "stop",
                            "stopwords": "_russian_"
                        },
                        "russian_stemmer": {
                            "type": "stemmer",
                            "language": "russian"
                        }
                    },
                    "analyzer": {
                        "ru_en": {
                            "tokenizer": "standard",
                            "filter": [
                                "lowercase",
                                "english_stop",
                                "english_stemmer",
                                "english_possessive_stemmer",
                                "russian_stop",
                                "russian_stemmer"
                            ]
                        }
                    }
                }
            },
            "mappings": {
                "dynamic": "strict",
                "properties": {
                    "id2": {
                        "type": "keyword"
                    },
                    "full_name": {
                        "type": "text",
                         "fields": {
                            "raw": {
                                "type": "keyword"
                            }
                        }
                    }
                }
            }
        })


@backoff.on_exception(backoff.expo,
                      ElasticsearchException,
                      max_time=60)
def bulk_upsert_movies(movies: List[ElasticMovie]) -> None:
    """
    Отправить _bulk запрос в индекс с фильмами.
    """
    global elasticsearch

    es_bulk_body = []
    for movie in movies:
        es_bulk_body += [
            {
                'index': {
                    '_index': 'movies',
                    '_id': movie.id
                }
            },
            dataclasses.asdict(movie)
        ]

    response = elasticsearch.bulk(es_bulk_body)
    if response['errors'] is True:
        raise Exception('Failed to bulk update')


@backoff.on_exception(backoff.expo,
                      ElasticsearchException,
                      max_time=60)
def bulk_upsert_genres(genres: List[ElasticGenre]) -> None:
    """
    Отправить _bulk запрос в индекс с жанрами.
    """
    global elasticsearch

    es_bulk_body = []
    for genre in genres:
        es_bulk_body += [
            {
                'index': {
                    '_index': 'genres',
                    '_id': genre.id
                }
            },
            dataclasses.asdict(genre)
        ]

    response = elasticsearch.bulk(es_bulk_body)
    if response['errors'] is True:
        raise Exception('Failed to bulk update')


@backoff.on_exception(backoff.expo,
                      ElasticsearchException,
                      max_time=60)
def bulk_upsert_persons(persons: List[ElasticPerson]) -> None:
    """
    Отправить _bulk запрос в индекс с участниками.
    """
    global elasticsearch

    es_bulk_body = []
    for person in persons:
        es_bulk_body += [
            {
                'index': {
                    '_index': 'persons',
                    '_id': person.id
                }
            },
            dataclasses.asdict(person)
        ]

    response = elasticsearch.bulk(es_bulk_body)
    if response['errors'] is True:
        raise Exception('Failed to bulk update')
