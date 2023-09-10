from typing import Optional

from pydantic import BaseModel, Field, root_validator
from pydantic.functional_validators import field_validator, model_validator
from pydantic_core.core_schema import FieldValidationInfo

from src.settings import settings


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
    origin: str = Field(min_length=4, max_length=4)
    distance_to_origin: float = Field(gt=-1)
    destination: str = Field(min_length=4, max_length=4)
    distance_to_destination: float
    tsat: Optional[str] = Field(pattern=r"[0-9]{4}")
    squawk: Optional[str] = Field(
        pattern=r"[0-7]{4}", max_length=4, min_length=4)
    sid: Optional[str]
    star: Optional[str]
    status: Optional[str]
    pressure_altitude: int
    flight_level: int
    stand: Optional[str]

    # noinspection PyNestedDecorators
    @model_validator(mode="after")
    def validate_prefix(self):
        if (self.origin and not self.origin.startswith(settings.airport_prefix)
                and not self.destination.startswith(settings.airport_prefix)):
            raise ValueError(f"Either the destination's ICAO code or the origin's " +
                             f"ICAO code should start with \"{settings.airport_prefix}\"")
        return self


class FlightCreate(FlightBase):
    pass


class FlightGet(FlightBase):
    last_updated: int
    callsign: Optional[str]
    origin: Optional[str]
    distance_to_origin: Optional[float]
    distance_to_destination: Optional[float]
    pressure_altitude: Optional[int]
    flight_level: Optional[int]


class Flight(FlightBase):
    last_updated: int

    class Config:
        from_attributes = True  # replacement for orm_mode
