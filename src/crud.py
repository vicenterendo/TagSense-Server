from sqlalchemy.orm import Session
from typing import Any
from . import models, schemas, utils, live_flights
from .settings import settings
import time

def get_flight(db: Session, valid_only = False, **kwargs: Any):
  all_flights = get_flights(db, valid_only=valid_only, **kwargs)
  return all_flights[0] if len(all_flights) > 0 else None

def get_flights(db: Session, valid_only = False, **kwargs: Any) -> list[models.Flight]:
  flights: list[models.Flight] = []
  for flight in db.query(models.Flight).filter_by(**kwargs).all():
    if (valid_only and utils.validate_flight(flight)) or not valid_only: flights.append(flight)
  return flights

def new_flight(db: Session, flight: schemas.FlightCreate):
  if flight.callsign == "EZY48MK":
    pass
  live_flight = live_flights.get_live_flight(callsign=flight.callsign)
  if live_flight is None: return None
  existing_flight = get_flight(db, uid=live_flight.uid)
  if existing_flight: return None
  db_flight = models.Flight(**flight.model_dump(), uid=live_flight.uid)
  if settings.validate_store and not utils.validate_flight(db_flight): return None
  db.add(db_flight)
  db.commit()
  db.refresh(db_flight)
  return db_flight

def set_flight(db: Session, flight: schemas.FlightCreate):
  live_flight = live_flights.get_live_flight(callsign=flight.callsign)
  existing_flight = get_flight(db, uid=live_flight.uid) if live_flight else None 
  for attr_name, attr_value in flight:
    if type(attr_value) != int and type(attr_value) != float and not attr_value: setattr(flight, attr_name, None)
  if existing_flight:
    existing_flight.last_updated = round(time.time())
    for column_name, value in flight.model_dump().items():
      if value is not None:
        setattr(existing_flight, column_name, value)
    db.commit()
    return existing_flight
  elif live_flight:
    db_flight = new_flight(db, flight)
    return db_flight if db_flight else None