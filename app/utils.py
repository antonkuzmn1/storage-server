import os
import shutil
from pathlib import Path
from uuid import uuid4
from fastapi import UploadFile

from settings import settings


UPLOAD_DIR = settings.UPLOAD_DIR

Path(UPLOAD_DIR).mkdir(parents=True, exist_ok=True)


def save_file(file: UploadFile):
    file_id = str(uuid4())
    file_location = os.path.join(UPLOAD_DIR, file_id)

    with open(file_location, "wb") as f:
        shutil.copyfileobj(file.file, f)

    return file_id, file_location
