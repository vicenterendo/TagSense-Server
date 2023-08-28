import time
from . import schemas, live_flights
from .settings import settings
import sys

def close(exit_code: int | None = None):
  settings.closed = True
  sys.exit(exit_code)

def validate_flight_age(flight_last_updated: int):
  return time.time() - flight_last_updated <= settings.max_age if settings.max_age else True

def validate_flight_airports(flight_origin: str, flight_destination: str):
  return flight_origin.startswith(settings.airport_prefix) or flight_destination.startswith(settings.airport_prefix)

def validate_flight_squawk(flight_squawk: str | None):
  if flight_squawk is not None:
    if "8" in flight_squawk or "9" in flight_squawk: return False
    if len(flight_squawk) != 4: return False
    return True
  else: 
    if settings.require_squawk: return False
    return True

def validate_flight_arrival(pressure_altitude: int, distance_to_origin: float, distance_to_destination: float):
  if settings.ignore_arrived and pressure_altitude < 100 and distance_to_destination < distance_to_origin: return False
  else: return True

def validate_flight(flight: schemas.Flight):
  if not validate_flight_age(flight.last_updated): return False
  if not validate_flight_airports(flight.origin, flight.destination): return False
  if not validate_flight_squawk(flight.squawk): return False
  if not validate_flight_arrival(flight.pressure_altitude, flight.distance_to_origin, flight.distance_to_destination): return False
  return True