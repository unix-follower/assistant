from contextlib import asynccontextmanager

from fastapi import FastAPI, Request
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
from fastapi_healthchecks.api.router import HealthcheckRouter, Probe

from app.config.config import Settings
from app.config.log_settings import configure_logging
from app.errors.app_exception import AppException
from app.errors.error_code import ErrorCode, to_http_status_code
from app.models.common import AppVersionModel

configure_logging()


def configure_healthcheck(fastapi_app: FastAPI):
    fastapi_app.include_router(
        HealthcheckRouter(
            Probe(
                name="readiness",
                checks=[],
            ),
            Probe(
                name="liveness",
                checks=[],
            ),
        ),
        prefix="/health",
    )


def configure_router(fastapi_app: FastAPI):
    configure_healthcheck(fastapi_app)


@asynccontextmanager
async def configure_app(fastapi_app: FastAPI):
    configure_router(fastapi_app)
    yield


origins = [
    "http://localhost",
    "http://localhost:3000",
]

settings = Settings()
app = FastAPI(
    title="assistant",
    version=settings.version,
    lifespan=configure_app,
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["POST", "GET"],
    allow_headers=["*"],
)


@app.get("/version", response_model=AppVersionModel)
async def get_version():
    return AppVersionModel(version=settings.version)


@app.exception_handler(Exception)
async def handle_exception(_: Request, e: Exception):
    error_code = ErrorCode.UNKNOWN
    if isinstance(e, AppException):
        error_code = e.error_code

    return JSONResponse(
        content={"errorCode": error_code.value},
        status_code=to_http_status_code(error_code),
    )
