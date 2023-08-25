from pydantic import BaseModel

class SimawareFlight(BaseModel):
  callsign: str
  cid: int
  dep: str
  arr: str
  lat: float
  lon: float
  alt: int
  crzalt: str
  aircraft: str
  route: str
  gndspd: int
  hdg: int
  uid: str
  name: str
  rating: int
  departed_at: str | None
  arrived_at: str | None

class FlightBase(BaseModel):
  callsign: str
  origin: str
  distance_to_origin: float
  destination: str
  distance_to_destination: float
  tsat: str | None
  squawk: str | None
  sid: str | None
  star: str | None
  status: str | None
  pressure_altitude: int
  flight_level: int
  
class FlightCreate(FlightBase):
  pass

class FlightGet(FlightBase):
  uid: str
  last_updated: int

class Flight(FlightBase):
  uid: str
  last_updated: int
  
  class Config:
    from_attributes = True  # replacement for orm_mode