from fastapi import APIRouter, Depends, HTTPException, Request, Response
from sqlalchemy.orm import Session

from src import crud, dependencies, schemas
from src.settings import settings

flights_router = APIRouter()


@flights_router.post("/flights")
def post_tag(res: Response, req: Request, body: list[schemas.FlightCreate], db: Session = Depends(dependencies.get_db)):
    flights: list[schemas.Flight] = []
    for flight_schema in body:
        db_flight = crud.set_flight(db, flight_schema)
        if not db_flight:
            continue
        dict_flight = db_flight.__dict__
        dict_flight.pop("_sa_instance_state")
        if not dict_flight:
            continue
        flights.append(schemas.Flight(**dict_flight))
    return flights


@flights_router.get("/flight/{callsign}", response_model=schemas.FlightGet)
def get_tag(callsign: str, res: Response, req: Request, db: Session = Depends(dependencies.get_db)):
    flight = crud.get_flight(db, callsign)
    return flight


@flights_router.get("/flights", response_model=list[schemas.FlightGet])
def get_all_tags(res: Response, req: Request, db: Session = Depends(dependencies.get_db),
                 max_age: int = settings.max_age):
    if not max_age >= 0:
        raise HTTPException(
            status_code=400, detail=[{
                "type": "value_error",
                "loc": ["query", "max_age"],
                "input": max_age,
                "msg": "Input should be equal or greater to 0."
            }], )
    flights = crud.get_flights(db, active_only=max_age)
    return flights
