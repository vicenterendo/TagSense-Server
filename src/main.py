import uvicorn, os, sys, time, threading, dotenv, argparse
from fastapi import FastAPI
from typing import List
from . import settings
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
  if not os.path.exists("private"): os.mkdir("private")
  from . import models
  from . import database
  from . import routers

  models.Base.metadata.create_all(bind=database.engine)

  app = FastAPI()
  app.include_router(routers.router, prefix="")

  @app.on_event("shutdown")
  async def app_shutdown():
    settings.settings.closed = True
    
  uvicorn.run(app, host=settings.settings.hostname, port=settings.settings.port, log_level="info")