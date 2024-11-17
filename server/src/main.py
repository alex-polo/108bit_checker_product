import logging
import os
from contextlib import asynccontextmanager

import yaml
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.middleware.httpsredirect import HTTPSRedirectMiddleware

from src.auth.routers import auth_router
from src.events.startup import up_server
from src.routes import store_router, catalog_router

logger = logging.getLogger('server')

origins = [
    "https://127.0.0.1:8080",
    "https://localhost:8080",
]

def config_logger() -> None:
    if not os.path.exists('logs'):
        os.mkdir('logs')

    with open('logging_config.yaml', 'r') as f:
        config = yaml.safe_load(f)
        logging.config.dictConfig(config)

@asynccontextmanager
async def lifespan(app: FastAPI):
    config_logger()
    await up_server()
    logger.info('Start server')
    yield
    pass

def get_version_app() -> str:
    try:
        with open('version.txt', 'r') as file:
            return file.read()
    except Exception as error:
        logger.error(error)
        return 'no-version'

app = FastAPI(
        title='108bit server',
        version=get_version_app(),
        lifespan=lifespan,
        docs_url="/server-docs",
        redoc_url="/server-redoc",
        openapi_url="/server-108bit-openapi.json"
    )


app.include_router(store_router)
app.include_router(catalog_router)
app.include_router(auth_router)

# app.add_middleware(HTTPSRedirectMiddleware, )
app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["GET", "POST"],
    allow_headers=["*"],
)