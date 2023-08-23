from fastapi import APIRouter
from fastapi import FastAPI, Response, Request
from typing import List
from pydantic import BaseModel
from ..database import SessionLocal
from .. import models, schemas, crud, utils

router = APIRouter()

@router.post("/tag", status_code=200)
def post_tag(res: Response, req: Request, body: List[schemas.FlightCreate]):
  session = SessionLocal()
  for flight_schema in body:
    crud.set_flight(session, flight_schema)
  session.close()

@router.get("/tag/{callsign}", status_code=200)
def get_tag(callsign: str, res: Response, req: Request):
  session = SessionLocal()
  flight = crud.get_flight(session, callsign)
  if flight: return flight
  else:
    res.status_code = 404
    return None

@router.get("/tag", status_code=200)
def get_all_tags(res: Response, req: Request):
  session = SessionLocal()
  flights = crud.get_flights(session)
  session.close()
  return flights