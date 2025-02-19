from typing import List

from sqlalchemy.orm import Session
from sqlalchemy.exc import SQLAlchemyError
from app.models import File
from app.logger import logger


class FileRepository:
    def __init__(self, db: Session):
        self.db = db

    def create_file(self, file_data: dict) -> File:
        try:
            db_file = File(**file_data)
            self.db.add(db_file)
            self.db.commit()
            self.db.refresh(db_file)
            return db_file
        except SQLAlchemyError as e:
            logger.error(f"Error creating item: {e}")
            self.db.rollback()
            return None

    def get_file(self, file_uuid: str) -> File:
        return self.db.query(File).filter(File.uuid == file_uuid).first()

    def get_all_files(self) -> List[File]:
        return self.db.query(File).all()

    def delete_file(self, file_uuid: str) -> None:
        db_file = self.get_file(file_uuid)
        if db_file:
            self.db.delete(db_file)

        try:
            self.db.commit()
            return db_file
        except SQLAlchemyError as e:
            logger.error(f"Error creating item: {e}")
            self.db.rollback()
            return None