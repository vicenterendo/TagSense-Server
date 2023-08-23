import uvicorn, os, sys, time, threading, dotenv
from . import globals
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

def run(argv: List[str]):
  __prefix_arg = find_arg("pfx", argv)
  
  try:
    globals.ORIGIN_PREFIX = os.getenv("TAGSENSE_ORIGIN_PREFIX", "") # The ICAO code of every flight's origin should start with this value
    globals.HOSTNAME = os.getenv("TAGSENSE_HOSTNAME", "0.0.0.0")
    globals.PORT = int(os.getenv("TAGSENSE_PORT", "80"))
    globals.DATABASE_URL = os.getenv("TAGSENSE_DATABASE_URL", "sqlite:///tagsense.db")
    globals.REQUIRE_SQUAWK = bool(int(os.getenv("TAGSENSE_REQUIRE_SQUAWK", "0")))
    globals.CLOSED = False
  except ValueError:
    print("ERR: Failed to parse an environment variable. Check if all environment variables can be parsed to meet their function.")
    return
  
  if not os.path.exists("private"): os.mkdir("private")
  from src.routers import tag

  from . import models, schemas, database, crud, utils

  models.Base.metadata.create_all(bind=database.engine)

  app = FastAPI()
  app.include_router(tag.router, prefix="")

  @app.on_event("shutdown")
  async def app_shutdown():
    globals.CLOSED = True

  def cleaner():
    skipped_iterations = 0
    while True:
      time.sleep(1)
      
      if globals.CLOSED: break
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
  uvicorn.run(app, host=globals.HOSTNAME, port=globals.PORT, log_level="info")