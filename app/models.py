from sqlalchemy import Column, Integer, String, DateTime, func, BigInteger
from sqlalchemy.orm import declarative_base

Base = declarative_base()


class File(Base):
    __tablename__ = 'files'

    uuid = Column(String(36), primary_key=True, index=True)
    name = Column(String(255), nullable=False)
    size = Column(BigInteger, nullable=False)
    user_id = Column(Integer, nullable=False)
    created_at = Column(DateTime, server_default=func.now())
    updated_at = Column(DateTime, onupdate=func.now())
