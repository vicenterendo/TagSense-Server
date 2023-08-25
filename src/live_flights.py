import threading
import time
from typing import Any
import requests
from . import schemas, utils
from .settings import settings

cache: list[schemas.SimawareFlight] = []

def get_live_flights() -> list[schemas.SimawareFlight]:
  return cache

def get_live_flight(**kwargs: Any) -> schemas.SimawareFlight | None:
  live_flights = get_live_flights()
  for arg_name in kwargs:
    for live_flight in live_flights:
      if live_flight.__dict__[arg_name] and live_flight.__dict__[arg_name] == kwargs[arg_name]:
        return live_flight
  return None

def __get_live_flights() -> list[schemas.SimawareFlight]:
  data: dict[str, Any] = requests.get("https://api2.simaware.ca/api/livedata/live.json").json()
  return [schemas.SimawareFlight(**data[value_name]) for value_name in data]

def __cache_updater():
  global cache
  skipped_iterations = 59
  while True:
    try:
      time.sleep(1)
      if settings.closed: break
      skipped_iterations += 1
      
      if skipped_iterations != 60: continue
      skipped_iterations = 0
    
      cache = __get_live_flights()
      
    except Exception as e:
      utils.print_error("LIVE FLIGHTS CACHE UPDATER", e)
      
threading.Thread(target=__cache_updater).start()