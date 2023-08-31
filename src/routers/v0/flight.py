from fastapi import APIRouter, Depends
from fastapi import Response, Request
from ... import schemas, crud, dependencies
from sqlalchemy.orm import Session

router = APIRouter()


@router.post("/flight")
def post_tag(res: Response, req: Request, body: list[schemas.FlightCreate], db: Session = Depends(dependencies.get_db)):
    flight: list[schemas.Flight] = []
    for flight_schema in body:
        db_flight = crud.set_flight(db, flight_schema)
        if not db_flight:
            continue
        dict_flight = db_flight.__dict__
        dict_flight.pop("_sa_instance_state")
        if not dict_flight:
            continue
        flight.append(schemas.Flight(**dict_flight))
    return flight


@router.get("/flight/{callsign}", response_model=list[schemas.FlightGet])
def get_tag(callsign: str, res: Response, req: Request, db: Session = Depends(dependencies.get_db)):
    flights = crud.get_flights(db, valid_only=True, callsign=callsign)
    return flights


@router.get("/flight", response_model=list[schemas.FlightGet])
def get_all_tags(res: Response, req: Request, db: Session = Depends(dependencies.get_db)):
    flights = crud.get_flights(db, valid_only=True)
    return flights
