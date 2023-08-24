import uvicorn, os, sys, time, threading, dotenv, argparse
import settings
from fastapi import FastAPI
from typing import List
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
  
  settings.load()
  
  if not os.path.exists("private"): os.mkdir("private")
  from src.routers import tag

  from . import models, schemas, database, crud, utils

  models.Base.metadata.create_all(bind=database.engine)

  app = FastAPI()
  app.include_router(tag.router, prefix="")

  @app.on_event("shutdown")
  async def app_shutdown():
    settings.settings.closed = True

  def cleaner():
    skipped_iterations = 0
    while True:
      time.sleep(1)
      
      if settings.settings.closed: break
      skipped_iterations += 1
      
      if skipped_iterations != 10: continue
      skipped_iterations = 0
      
      session = database.SessionLocal()
      flights = crud.get_flights(session)
      
      for flight in flights:
        if not utils.is_flight_valid(flight):
          session.delete(flight)
          
      session.commit()
      session.close()

  threading.Thread(target=cleaner).start()
  uvicorn.run(app, host=settings.settings.hostname, port=settings.settings.port, log_level="info")