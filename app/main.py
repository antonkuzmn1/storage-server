from pathlib import Path

from fastapi import FastAPI

from app.settings import settings
from app.api import router

UPLOAD_DIR = "uploads"

Path(UPLOAD_DIR).mkdir(parents=True, exist_ok=True)

app = FastAPI()

app.include_router(router)


@app.get("/")
def main():
    return {
        "message": "test!",
        "debug": settings.DEBUG,
        "test": 1,
    }
