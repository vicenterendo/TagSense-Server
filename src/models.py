from sqlalchemy import Column,  Integer, String, Float
from .database import Base
import time


class Flight(Base):
    __tablename__ = "flights"
    uid = Column(String(255), primary_key=True)
    callsign = Column(String(255))
    origin = Column(String(4))
    distance_to_origin = Column(Float)
    destination = Column(String(4))
    distance_to_destination = Column(Float)
    tsat = Column(String(4), nullable=True)
    squawk = Column(String(4), nullable=True)
    sid = Column(String(255), nullable=True)
    star = Column(String(255), nullable=True)
    status = Column(String(255), nullable=True)
    stand = Column(String(255), nullable=True)
    pressure_altitude = Column(Integer)
    flight_level = Column(Integer)
    last_updated = Column(Integer)

    def __init__(
        self,
        uid: str,
        callsign: str,
        origin: str,
        distance_to_origin: float,
        destination: str,
        distance_to_destination: float,
        pressure_altitude: int,
        flight_level: int,
        tsat: str | None,
        squawk: str | None,
        sid: str | None,
        star: str | None,
        status: str | None,
        stand: str | None
    ):
        self.uid = uid
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
        self.stand = stand
        self.last_updated = round(time.time())
