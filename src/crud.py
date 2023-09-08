import time
from typing import Any, Optional, Iterator, List, Type

from sqlalchemy.orm import Session

from . import models, schemas, utils
from .models import Flight
from .settings import settings


def get_flight(db: Session, callsign: str) -> Optional[models.Flight]:
    return db.query(models.Flight).filter_by(callsign=callsign).first()


def get_flights(db: Session, active_only: int = settings.max_age) -> list[Type[Flight]]:
    flights: list[Type[Flight]] = db.query(models.Flight).all()

    if active_only:
        flights = [flight for flight in flights if (time.time() - flight.last_updated) < active_only]
    return flights


def set_flight(db: Session, flight: schemas.FlightCreate):
    existing_flight = get_flight(db, flight.callsign)
    if existing_flight:
        for column_name, new_value in flight.model_dump().items():
            if new_value is not None:
                setattr(existing_flight, column_name, new_value)
        existing_flight.last_updated = round(time.time())
        db.commit()
        return existing_flight
    else:
        db_flight = models.Flight(**flight.model_dump())
        if settings.validate_store and not utils.validate_flight(db_flight):
            return None
        db.add(db_flight)
        db.commit()
        db.refresh(db_flight)
        return db_flight
