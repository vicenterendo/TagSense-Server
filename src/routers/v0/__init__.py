from fastapi import APIRouter
from . import flight
router = APIRouter()
router.include_router(flight.router)
