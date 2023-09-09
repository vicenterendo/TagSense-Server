import time

import dotenv
import pymysql
import sqlalchemy.exc
import uvicorn
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from src import logs, settings
from src.routers.main import router

dotenv.load_dotenv()
logger = logs.get_logger(__name__)


def run():
    from . import database, models, routers, utils

    logger.info(f"Connecting to DB at \"{settings.settings.database_url}\"...")
    fails = 0
    while True:
        try:
            models.Base.metadata.create_all(bind=database.engine)
            break
        except sqlalchemy.exc.OperationalError or pymysql.err.OperationalError:
            fails += 1
            if fails >= settings.settings.db_max_attempts:
                logger.critical(
                    f"Failed to connect to DB. [{fails}/{settings.settings.db_max_attempts}] (max attempts reached)")
                utils.close(-1)
            logger.error(
                f"Failed to connect to DB, retrying... [{fails}/{settings.settings.db_max_attempts}]")
            time.sleep(2)

    logger.info(f"Successfully connected to DB")
    app = FastAPI()
    if settings.settings.cors:
        app.add_middleware(CORSMiddleware, allow_origins=settings.settings.cors,
                           allow_credentials=True, allow_methods=["*"], allow_headers=["*"])
    app.include_router(router, prefix="")

    uvicorn.run(app, host=settings.settings.hostname,
                port=settings.settings.port, log_level="info")
    utils.close()
