import time
from . import schemas
from .settings import settings
import sys

def close(exit_code: int | None = None):
  settings.closed = True
  sys.exit(exit_code)

def is_flight_age_valid(flight_last_updated: int):
  return time.time() - flight_last_updated <= settings.max_age if settings.max_age else True

def is_flight_origin_valid(flight_origin: str):
  return flight_origin.startswith(settings.origin_prefix)

def is_flight_squawk_valid(flight_squawk: str | None):
  if flight_squawk is not None:
    if "8" in flight_squawk or "9" in flight_squawk: return False
    if len(flight_squawk) != 4: return False
    return True
  else: 
    if settings.require_squawk: return False
    return True

def is_flight_valid(flight: schemas.Flight):
  if not is_flight_age_valid(flight.last_updated): return False
  if not is_flight_origin_valid(flight.origin): return False
  if not is_flight_squawk_valid(flight.squawk): return False
  return True

def print_error(context: str, e: Exception):
  print(f"--------- ERROR IN {context} ----------\n{e}")