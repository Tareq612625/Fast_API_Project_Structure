# Application entrypoint (FastAPI instance)
from fastapi import FastAPI
from app.core.dependencies import init_db
from app.api.v1.endpoints import user

app = FastAPI()

app.include_router(user.router, prefix="/users", tags=["users"])

# @app.on_event("startup")
# async def on_startup():
#     await init_db()

@app.get("/")
async def root():
    return {"message": "Hello World"}
