# Main API entrypoint (includes all versions)
from fastapi import FastAPI
from app.api.v1.endpoints import user

app = FastAPI()

app.include_router(user.router, prefix="/users", tags=["users"])
