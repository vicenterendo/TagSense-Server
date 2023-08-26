from fastapi import APIRouter
from fastapi import FastAPI, Response, Request
from typing import List
from pydantic import BaseModel
from ...database import SessionLocal
from ... import models, schemas, crud, utils

router = APIRouter()

@router.post("/flight")
def post_tag(res: Response, req: Request, body: list[schemas.FlightCreate]):
  flight: list[schemas.Flight] = []
  for flight_schema in body:
    session = SessionLocal()
    db_flight = crud.set_flight(session, flight_schema)
    if not db_flight: continue
    dict_flight = db_flight.__dict__
    dict_flight.pop("_sa_instance_state")
    if not dict_flight: continue
    flight.append(schemas.Flight(**dict_flight))
    session.close()
  return flight

@router.get("/flight/{callsign}", response_model=list[schemas.FlightGet])
def get_tag(callsign: str, res: Response, req: Request):
  session = SessionLocal()
  flights = crud.get_flights(session, valid_only=True, callsign=callsign)
  session.close()
  return flights

@router.get("/flight", response_model=list[schemas.FlightGet])
def get_all_tags(res: Response, req: Request):
  session = SessionLocal()
  flights = crud.get_flights(session, valid_only=True)
  session.close()
  return flights