from fastapi import APIRouter
from src.routers.v0.flights import flights_router

v0_router = APIRouter()
v0_router.include_router(flights_router)
