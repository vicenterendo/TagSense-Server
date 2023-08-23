from sqlalchemy.orm import Session
from typing import Any
from . import models, schemas, utils
import time

def get_flight(db: Session, flight_callsign: str):
  return db.query(models.Flight).filter_by(callsign = flight_callsign).first()

def get_flights(db: Session, **kwargs: Any):
  return db.query(models.Flight).filter_by(**kwargs).all()

def new_flight(db: Session, flight: schemas.FlightCreate):
  if get_flight(db, flight.callsign): return None
  for attr_name, attr_value in flight:
    attr_value = attr_value if attr_value else None
  db_flight = models.Flight(**flight.model_dump())
  if not utils.is_flight_valid(db_flight): return None
  db.add(db_flight)
  db.commit()
  db.refresh(db_flight)
  return db_flight

def set_flight(db: Session, flight: schemas.FlightCreate):
  existing_flight = get_flight(db, flight.callsign)
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