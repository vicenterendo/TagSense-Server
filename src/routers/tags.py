from fastapi import APIRouter
from fastapi import FastAPI, Response, Request
from typing import List
from pydantic import BaseModel
from ..database import Session, DFlight
from ..funcs import *
import time

router = APIRouter()

def int_if_able(input: str):
  try:
    return int(input)
  except:
    return None

def eval_param(param: str):
  if not param or param == "":
    return None
  else:
    return param

class OFlight(BaseModel):
  callsign: str
  tsat: str
  origin: str
  distance_to_origin: str
  destination: str
  distance_to_destination: str
  squawk: str
  sid: str
  star: str
  status: str
  flight_level: str
  pressure_altitude: str

@router.post("/tag", status_code=200)
def post_tag(res: Response, req: Request, body: List[OFlight]):
  session = Session()
  for flight in body:
    try:
      _flt = session.query(DFlight).filter_by(callsign=flight.callsign).first()
      _flt_ = {
        "callsign": flight.callsign,
        "origin": flight.origin,
        "distance_to_origin": round(float(flight.distance_to_origin), 2),
        "destination": flight.destination,
        "distance_to_destination": round(
          float(flight.distance_to_destination), 2
        ),
        "pressure_altitude": int(flight.pressure_altitude),
        "flight_level": int(flight.flight_level),
        "tsat": int_if_able(flight.tsat),
        "squawk": int_if_able(flight.squawk),
        "sid": eval_param(flight.sid),
        "star": eval_param(flight.star),
        "status": eval_param(flight.status),
        "last_updated": round(time.time()),
      }
      if _flt:
        if not validate_flt(_flt): 
          session.delete(_flt)
          continue
        _flt.last_updated = round(time.time())
        for column_name, value in _flt_.items():
          try:
            if value is not None:
              setattr(_flt, column_name, value)
          except:
            pass
      else:
        flt = DFlight(
          _flt_["callsign"],
          _flt_["origin"],
          _flt_["distance_to_origin"],
          _flt_["destination"],
          _flt_["distance_to_destination"],
          _flt_["pressure_altitude"],
          _flt_["flight_level"],
          _flt_["tsat"],
          _flt_["squawk"],
          _flt_["sid"],
          _flt_["star"],
          _flt_["status"],
        )
        if validate_flt(flt):
          session.add(flt)
    except:
      print("ERR")
  session.commit()
  session.close()

@router.get("/tag/{callsign}", status_code=200)
def get_tag(callsign: str, res: Response, req: Request):
  session = Session()
  flt = session.query(DFlight).filter_by(callsign=callsign).first()
  if flt:
    return flt
  else:
    res.status_code = 404
    return None

@router.get("/tag", status_code=200)
def get_all_tags(res: Response, req: Request):
  session = Session()
  flts = session.query(DFlight).all()
  session.close()
  return flts