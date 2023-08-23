from sqlalchemy import Column,  Integer, String, Float
from .database import Base
import time

class Flight(Base):
  __tablename__ = "flights"
  callsign = Column(String, primary_key=True)
  origin = Column(String)
  distance_to_origin = Column(Float)
  destination = Column(String)
  distance_to_destination = Column(Float)
  tsat = Column(String, nullable=True)
  squawk = Column(String, nullable=True)
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