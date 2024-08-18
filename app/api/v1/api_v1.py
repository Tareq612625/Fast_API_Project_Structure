# API version 1 entrypoint (including all routes)
from fastapi import APIRouter
from app.api.v1.endpoints import user

api_v1_router = APIRouter()

api_v1_router.include_router(user.router, prefix="/users", tags=["users"])

