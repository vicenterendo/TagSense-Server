from sqlalchemy.orm import Session
from typing import Any
from . import models, schemas, utils, live_flights
import time

def get_flight(db: Session, **kwargs: Any):
  return db.query(models.Flight).filter_by(**kwargs).first()

def get_flights(db: Session, **kwargs: Any):
  return db.query(models.Flight).filter_by(**kwargs).all()



def new_flight(db: Session, flight: schemas.FlightCreate):
  live_flight = live_flights.get_live_flight(callsign=flight.callsign)
  if live_flight is None or get_flight(db, uid=live_flight.uid): return None
  db_flight = models.Flight(**flight.model_dump(), uid=live_flight.uid)
  if not utils.is_flight_valid(db_flight): return None
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
  else:
    db_flight = new_flight(db, flight)
    return db_flight if db_flight else None