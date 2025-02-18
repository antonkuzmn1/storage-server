import os
import shutil
from pathlib import Path
from uuid import uuid4

from fastapi import UploadFile


UPLOAD_DIR = "uploads"

Path(UPLOAD_DIR).mkdir(parents=True, exist_ok=True)


def save_file(file: UploadFile):
    file_id = str(uuid4())
    file_location = os.path.join(UPLOAD_DIR, file_id)

    with open(file_location, "wb") as f:
        shutil.copyfileobj(file.file, f)

    return file_id, file_location
