from fastapi import FastAPI, File, UploadFile, HTTPException
from fastapi.responses import FileResponse
from fastapi import Request
import os
import shutil
from uuid import uuid4
from pathlib import Path

UPLOAD_DIR = "uploads"

Path(UPLOAD_DIR).mkdir(parents=True, exist_ok=True)

app = FastAPI()


def save_file(file: UploadFile):
    file_id = str(uuid4())
    file_location = os.path.join(UPLOAD_DIR, file_id)

    with open(file_location, "wb") as f:
        shutil.copyfileobj(file.file, f)

    return file_id, file_location


@app.post("/upload/")
async def upload_file(file: UploadFile = File(...)):
    try:
        file_id, file_location = save_file(file)
        return {"file_id": file_id, "file_location": file_location}
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error saving file: {str(e)}")


@app.get("/download/{file_id}")
async def download_file(file_id: str):
    file_path = os.path.join(UPLOAD_DIR, file_id)

    if not os.path.exists(file_path):
        raise HTTPException(status_code=404, detail="File not found")

    return FileResponse(file_path)


@app.delete("/delete/{file_id}")
async def delete_file(file_id: str):
    file_path = os.path.join(UPLOAD_DIR, file_id)

    if not os.path.exists(file_path):
        raise HTTPException(status_code=404, detail="File not found")

    os.remove(file_path)
    return {"message": "File deleted successfully"}