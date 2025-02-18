from fastapi import FastAPI

from app.api import router
from app.settings import settings

app = FastAPI()

app.include_router(router)


@app.get("/")
def main():
    return {
        "message": "test!",
        "debug": settings.DEBUG,
        "test": 2,
    }
