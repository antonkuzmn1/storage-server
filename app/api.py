from fastapi import APIRouter, Depends, UploadFile, File, HTTPException, status
from fastapi.responses import FileResponse
from sqlalchemy.ext.asyncio import AsyncSession

from app.db import get_db
from app.dependencies.auth import verify_token, require_roles
from app.schemas.file import FileOut
from app.services.file_service import FileService
from app.repositories.file_repo import FileRepository
from app.settings import settings

router = APIRouter(tags=["files"])



async def get_file_service(db: AsyncSession = Depends(get_db)) -> FileService:
    return FileService(
        repository=FileRepository(db),
        upload_dir=settings.UPLOAD_DIR
    )


@router.post("/upload", response_model=FileOut)
async def upload_file(
        file: UploadFile = File(...),
        service: FileService = Depends(get_file_service),
        user_data: dict = Depends(verify_token),
):
    try:
        return await service.save_upload_file(file, user_data["id"])
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=f"File upload failed: {str(e)}"
        )


@router.get("/download/{file_uuid}")
async def download_file(
        file_uuid: str,
        service: FileService = Depends(get_file_service),
        user_data: dict = Depends(verify_token)
):
    try:
        file_info = await service.verify_file_access(
            file_uuid,
            str(user_data["id"]),
            roles=[user_data.get("role")]
        )
        file_path = await service.get_file_path(file_uuid)

        if not file_path:
            raise HTTPException(404, detail="File not found")

        return FileResponse(
            file_path,
            filename=file_info.name,
            headers={"Content-Length": str(file_info.size)}
        )
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(500, detail=str(e))


@router.delete("/delete/{file_uuid}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_file(
    file_uuid: str,
    service: FileService = Depends(get_file_service),
    _: dict = require_roles(["owner"])
):
    if not await service.delete_file(file_uuid):
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="File not found"
        )