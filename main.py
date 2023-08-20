import uvicorn, os, sys, json, time, threading, secrets
from fastapi import FastAPI, Response, status, Header, Request
from pydantic import BaseModel
from typing import List
from sqlalchemy import (
  MetaData,
  Table,
  create_engine,
  ForeignKey,
  Column,
  String,
  Integer,
  CHAR,
  Float,
)
from sqlalchemy.orm import sessionmaker, declarative_base

if not os.path.exists("private"):
  os.mkdir("private")
Base = declarative_base()
last_update_time = round(time.time())

def find_arg(arg: str, argv: List[str]):
  for i, _arg in enumerate(argv):
    if (_arg == f"--{arg}") and (i + 1) < len(argv):
      return argv[i + 1]
  return None

__prefix_arg = find_arg("pfx", sys.argv)
ORIGIN_PREFIX = __prefix_arg if __prefix_arg is not None else "" # The ICAO code of every flight's origin should start with this value
CLOSED = False
__hostname_arg = find_arg("h", sys.argv)
HOSTNAME = __hostname_arg if __hostname_arg is not None else "0.0.0.0"
__port_arg = find_arg("p", sys.argv)
PORT = int(__port_arg) if __port_arg is not None else 80

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


class DInterface(Base):
  __tablename__ = "interface"
  cid = Column("cid", String, primary_key=True, nullable=False)
  started_at = Column("started_at", Integer, nullable=False)
  last_checkin = Column("last_checkin", Integer, nullable=False)
  token = Column("token", String, nullable=False)

  def __init__(
    self,
    cid: str,
    started_at: int = round(time.time()),
    last_checkin: int = round(time.time()),
    token: str = secrets.token_urlsafe(16),
  ):
    self.cid = cid
    self.started_at = started_at
    self.last_checkin = last_checkin
    self.token = token


class DFlight(Base):
  __tablename__ = "flights"
  # interface_cid = Column(Integer, ForeignKey("interface.cid", ondelete="CASCADE"), nullable=False)
  callsign = Column(String, primary_key=True)
  origin = Column(String)
  distance_to_origin = Column(Float)
  destination = Column(String)
  distance_to_destination = Column(Float)
  tsat = Column(Integer, nullable=True)
  squawk = Column(Integer, nullable=True)
  sid = Column(String, nullable=True)
  star = Column(String, nullable=True)
  status = Column(String, nullable=True)
  pressure_altitude = Column(Integer)
  flight_level = Column(Integer)
  last_updated = Column(Integer)

  def __init__(
    self,
    callsign: str,
    origin: str,
    distance_to_origin: float,
    destination: str,
    distance_to_destination: float,
    pressure_altitude: int,
    flight_level: int,
    tsat: int | None,
    squawk: int | None,
    sid: str | None,
    star: str | None,
    status: str | None,
  ):
    self.callsign = callsign
    self.tsat = tsat
    self.origin = origin
    self.distance_to_origin = distance_to_origin
    self.destination = destination
    self.distance_to_destination = distance_to_destination
    self.squawk = squawk
    self.sid = sid
    self.star = star
    self.status = status
    self.pressure_altitude = pressure_altitude
    self.flight_level = flight_level
    self.last_updated = round(time.time())


def is_flt_valid(flt: DFlight):
  if (last_update_time - int(str(flt.last_updated)) > 30) or float(
    str(flt.distance_to_destination)
  ) < float(str(flt.distance_to_origin)) or not str(flt.origin).startswith(ORIGIN_PREFIX):
    return False
  else:
    return True


def cleaner():
  passed = 0
  while True:
    time.sleep(1)
    if CLOSED: return
    passed += 1
    if passed != 10: continue
    passed = 0
    session = Session()
    flts = session.query(DFlight).all()
    for flt in flts:
      if not is_flt_valid(flt):
        session.delete(flt)
    session.commit()
    session.close()


app = FastAPI()
engine = create_engine("sqlite:///private/db.db")
Base.metadata.create_all(bind=engine)
Session = sessionmaker(bind=engine)
thread = threading.Thread(target=cleaner)
thread.start()


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


@app.post("/tag", status_code=200)
def home_post(res: Response, req: Request, body: List[OFlight]):
  global last_update_time
  session = Session()
  last_update_time = round(time.time())
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
        if not is_flt_valid(_flt): 
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
        if is_flt_valid(flt):
          session.add(flt)
    except:
      print("ERR")
  session.commit()
  session.close()


@app.get("/tag/{callsign}", status_code=200)
def tag_callsign_get(callsign: str, res: Response, req: Request):
  session = Session()
  flt = session.query(DFlight).filter_by(callsign=callsign).first()
  if flt:
    return flt
  else:
    res.status_code = 404
    return None


@app.get("/tag/", status_code=200)
def tag_get(res: Response, req: Request):
  session = Session()
  flts = session.query(DFlight).all()
  session.close()
  return flts


if __name__ == "__main__":
  uvicorn.run(app, host=HOSTNAME, port=PORT)
  CLOSED = True