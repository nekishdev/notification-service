import logging

import aioredis
import uvicorn as uvicorn
from elasticsearch import AsyncElasticsearch
from fastapi import FastAPI
from fastapi.responses import ORJSONResponse
from fastapi_jwt_auth import AuthJWT
from fastapi_jwt_auth.exceptions import AuthJWTException
from starlette.responses import JSONResponse

from api.v1 import films, genres, persons
from core.config import settings, JwtSettings
from core.logger import LOGGING
import db.elastic as elastic
import db.redis as redis

app = FastAPI(
    title=settings.PROJECT_NAME,
    docs_url='/api/openapi',
    openapi_url='/api/openapi.json',
    debug=settings.DEBUG,
    default_response_class=ORJSONResponse,
    description='Информация о фильмах, жанрах и людях, участвовавших в создании произведения',
    version='1.0.0',
)


@app.on_event('startup')
async def startup():
    redis.redis = await aioredis.create_redis_pool(
        (settings.REDIS_HOST, settings.REDIS_PORT), minsize=10, maxsize=20
    )
    elastic.es = AsyncElasticsearch(hosts=[f'{settings.ELASTIC_HOST}:{settings.ELASTIC_PORT}'])


@app.on_event('shutdown')
async def shutdown():
    await redis.redis.close()
    await elastic.es.close()


@AuthJWT.load_config
def get_config():
    return JwtSettings()


@app.exception_handler(AuthJWTException)
def authjwt_exception_handler(request, exc: AuthJWTException):
    return JSONResponse(
        status_code=exc.status_code,
        content={"detail": exc.message}
    )


app.include_router(
    films.router, prefix='/api/v1/films', tags=['Полнотекстовый поиск кинопроизведений']
)
app.include_router(genres.router, prefix='/api/v1/genres', tags=['Поиск жанров'])
app.include_router(
    persons.router,
    prefix='/api/v1/persons',
    tags=['Полнотекстовый поиск участников кинопроизведений'],
)

if __name__ == '__main__':
    uvicorn.run(
        'main:app',
        host=settings.FASTAPI_HOST,
        port=settings.FASTAPI_PORT,
        log_config=LOGGING,
        log_level=logging.DEBUG,
        reload=True,
    )
