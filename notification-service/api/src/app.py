import logging

import uvicorn
from fastapi import FastAPI
from fastapi.responses import ORJSONResponse
from fastapi_jwt_auth import AuthJWT
from fastapi_jwt_auth.exceptions import AuthJWTException
from starlette.responses import JSONResponse

from api.v1 import notify
from logger import LOGGING
from services.rmq import PikaClient
from settings import JwtSettings, settings

app = FastAPI(
    title=settings.PROJECT_NAME,
    docs_url="/docs",
    openapi_url="/api/openapi.json",
    debug=settings.DEBUG,
    # default_response_class=ORJSONResponse,
    description="API сервиса нотификаций",
    version="1.0.0",
)


@app.on_event("startup")
async def startup():
    await PikaClient.channel()


@app.on_event("shutdown")
async def shutdown():
    PikaClient.get_connection().close()


@AuthJWT.load_config
def get_config():
    return JwtSettings()


@app.exception_handler(AuthJWTException)
def authjwt_exception_handler(request, exc: AuthJWTException):
    return JSONResponse(status_code=exc.status_code, content={"detail": exc.message})


app.include_router(notify.router, prefix="/api/v1/notify", tags=["Notifications"])

if __name__ == "__main__":
    uvicorn.run(
        "app:app",
        host=settings.FASTAPI_HOST,
        port=settings.FASTAPI_PORT,
        log_config=LOGGING,
        log_level=logging.DEBUG,
        reload=True,
    )
