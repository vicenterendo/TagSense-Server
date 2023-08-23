import uvicorn, os, sys, time, threading
from . import globals
from fastapi import FastAPI
from typing import List

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
  globals.ORIGIN_PREFIX = __prefix_arg if __prefix_arg is not None else "" # The ICAO code of every flight's origin should start with this value
  __hostname_arg = find_arg("hostname", argv)
  globals.HOSTNAME = __hostname_arg if __hostname_arg is not None else "0.0.0.0"
  __port_arg = find_arg("port", argv)
  globals.PORT = int(__port_arg) if __port_arg is not None else 80
  __database_arg = find_arg("database", argv)
  globals.DATABASE_URL = __database_arg if __database_arg is not None else "sqlite:///private/db.db"
  globals.REQUIRE_SQUAWK = find_switch("sqwk", argv)
  globals.PORT = int(__port_arg) if __port_arg is not None else 80
  globals.CLOSED = False

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