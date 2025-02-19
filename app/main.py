from fastapi import FastAPI
from contextlib import asynccontextmanager

from app.api import router
from app.settings import settings
# from app.db import create_tables, drop_tables


@asynccontextmanager
async def lifespan(_app: FastAPI):
    print("Server started!")
    # await create_tables()
    yield
    print("Server stopped!")
app = FastAPI(lifespan=lifespan)

app.include_router(router)


@app.get("/")
def main():
    return {
        "message": "test!",
        "debug": settings.DEBUG,
        "test": 3,
    }
