from fastapi import APIRouter
from .endpoints import diagnostics

api_router = APIRouter()

api_router.include_router(
    diagnostics.router, 
    prefix="/diagnostics", 
    tags=["Diagnostics"]
)