import os

from fastapi import File, UploadFile, HTTPException, APIRouter
from fastapi.responses import FileResponse

from app.main import UPLOAD_DIR
from app.utils import save_file

router = APIRouter()


@router.post("/upload/")
async def upload_file(file: UploadFile = File(...)):
    try:
        file_id, file_location = save_file(file)
        return {"file_id": file_id, "file_location": file_location}
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error saving file: {str(e)}")


@router.get("/download/{file_id}")
async def download_file(file_id: str):
    file_path = os.path.join(UPLOAD_DIR, file_id)

    if not os.path.exists(file_path):
        raise HTTPException(status_code=404, detail="File not found")

    return FileResponse(file_path)


@router.delete("/delete/{file_id}")
async def delete_file(file_id: str):
    file_path = os.path.join(UPLOAD_DIR, file_id)

    if not os.path.exists(file_path):
        raise HTTPException(status_code=404, detail="File not found")

    os.remove(file_path)
    return {"message": "File deleted successfully"}
