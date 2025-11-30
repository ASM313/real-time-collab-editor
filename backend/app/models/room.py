from sqlalchemy import Column, String, Text, DateTime, Integer
from sqlalchemy.sql import func
from app.db.base import Base
from datetime import datetime


class Room(Base):
    """Model for storing room code and metadata."""
    
    __tablename__ = "rooms"
    
    room_id = Column(String(36), primary_key=True, index=True)
    code = Column(Text, default="", nullable=False)
    created_at = Column(DateTime, default=func.now(), nullable=False)
    updated_at = Column(DateTime, default=func.now(), onupdate=func.now(), nullable=False)
    active_users = Column(Integer, default=0, nullable=False)
    
    def __repr__(self) -> str:
        return f"<Room(room_id={self.room_id}, active_users={self.active_users})>"
