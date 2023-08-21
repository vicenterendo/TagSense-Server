from src.store import settings
import uvicorn, os, sys, time, threading
from fastapi import FastAPI, Response, Request
from pydantic import BaseModel
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
  settings.ORIGIN_PREFIX = __prefix_arg if __prefix_arg is not None else "" # The ICAO code of every flight's origin should start with this value
  __hostname_arg = find_arg("hostname", argv)
  settings.HOSTNAME = __hostname_arg if __hostname_arg is not None else "0.0.0.0"
  __port_arg = find_arg("port", argv)
  settings.PORT = int(__port_arg) if __port_arg is not None else 80
  __database_arg = find_arg("database", argv)
  settings.DATABASE_URL = __database_arg if __database_arg is not None else "sqlite:///private/db.db"
  settings.REQUIRE_SQUAWK = find_switch("sqwk", argv)
  settings.PORT = int(__port_arg) if __port_arg is not None else 80
  settings.CLOSED = False

  if not os.path.exists("private"):
    os.mkdir("private")

  from src import funcs
  from src import database
  from src.routers import tags

  app = FastAPI()
  app.include_router(tags.router, prefix="")

  @app.on_event("shutdown")
  async def app_shutdown():
    settings.CLOSED = True

  def cleaner():
    passed = 0
    while True:
      time.sleep(1)
      if settings.CLOSED: return
      passed += 1
      if passed != 10: continue
      passed = 0
      session = database.Session()
      flts = session.query(database.DFlight).all()
      for flt in flts:
        if not funcs.validate_flt(flt):
          session.delete(flt)
      session.commit()
      session.close()

  threading.Thread(target=cleaner).start()
  uvicorn.run(app, host=settings.HOSTNAME, port=settings.PORT, log_level="info")