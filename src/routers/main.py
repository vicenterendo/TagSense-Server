from fastapi import APIRouter
from src.routers.v0.main import v0_router

router = APIRouter()
router.include_router(v0_router, prefix="/v0")
