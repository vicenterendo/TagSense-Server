from pydantic import BaseModel

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

class Flight(FlightBase):
  last_updated: int
  
  class Config:
    from_attributes = True  # replacement for orm_mode