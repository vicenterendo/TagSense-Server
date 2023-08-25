from fastapi import APIRouter
from fastapi import FastAPI, Response, Request
from typing import List
from pydantic import BaseModel
from ...database import SessionLocal
from ... import models, schemas, crud, utils

router = APIRouter()

@router.post("/flight", response_model=schemas.FlightBase)
def post_tag(res: Response, req: Request, body: List[schemas.FlightCreate]):
  session = SessionLocal()
  for flight_schema in body:
    crud.set_flight(session, flight_schema)
  session.close()

@router.get("/flight/{callsign}", response_model=list[schemas.FlightBase])
def get_tag(callsign: str, res: Response, req: Request):
  session = SessionLocal()
  flights = crud.get_flights(session, callsign=callsign)
  session.close()
  return flights

@router.get("/flight", response_model=list[schemas.FlightBase])
def get_all_tags(res: Response, req: Request):
  session = SessionLocal()
  flights = crud.get_flights(session)
  session.close()
  return flights