import uvicorn
import os
import sys
import time
import threading
import dotenv
import argparse
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from typing import List
import sqlalchemy.exc
import pymysql
import cryptography
from . import settings, logging
dotenv.load_dotenv()


def find_arg(arg: str, argv: List[str]):
    for i, _arg in enumerate(argv):
        if (_arg == f"--{arg}") and (i + 1) < len(argv) and not argv[i + 1].startswith("-"):
            return argv[i + 1]
    return None


def find_switch(switch: str, argv: List[str]) -> bool:
    for i, _switch in enumerate(argv):
        if (_switch == f"-{switch}"):
            return True
    return False


def run():
    if not os.path.exists("private"):
        os.mkdir("private")
    from . import models
    from . import database
    from . import routers
    from . import utils

    logging.logger.info(
        f"Connecting to DB at \"{settings.settings.database_url}\"...")
    fails = 0
    while True:
        try:
            models.Base.metadata.create_all(bind=database.engine)
            break
        except sqlalchemy.exc.OperationalError or pymysql.err.OperationalError:
            fails += 1
            if fails >= settings.settings.db_max_attempts:
                logging.logger.critical(
                    f"Failed to connect to DB. [{fails}/{settings.settings.db_max_attempts}] (max attempts reached)")
                utils.close(-1)
            logging.logger.error(
                f"Failed to connect to DB, retrying... [{fails}/{settings.settings.db_max_attempts}]")
            time.sleep(2)

    logging.logger.info(f"Successfully connected to DB")
    app = FastAPI()
    if settings.settings.cors:
        app.add_middleware(CORSMiddleware, allow_origins=settings.settings.cors,
                           allow_credentials=True, allow_methods=["*"], allow_headers=["*"])
    app.include_router(routers.router, prefix="")

    uvicorn.run(app, host=settings.settings.hostname,
                port=settings.settings.port, log_level="info")
    utils.close()
