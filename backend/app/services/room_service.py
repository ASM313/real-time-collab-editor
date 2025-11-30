from sqlalchemy.orm import Session
from app.models.room import Room
from datetime import datetime


class RoomService:
    """Service for managing rooms and their code state."""
    
    def __init__(self, db: Session):
        self.db = db
    
    def create_room(self, room_id: str) -> Room:
        """
        Create a new room.
        
        Args:
            room_id: Unique identifier for the room
            
        Returns:
            Room: The created room object
        """
        room = Room(room_id=room_id, code="", active_users=0)
        self.db.add(room)
        self.db.commit()
        self.db.refresh(room)
        return room
    
    def get_room(self, room_id: str) -> Room | None:
        """
        Get a room by ID.
        
        Args:
            room_id: The room identifier
            
        Returns:
            Room or None: The room object or None if not found
        """
        return self.db.query(Room).filter(Room.room_id == room_id).first()
    
    def update_code(self, room_id: str, code: str) -> Room | None:
        """
        Update the code in a room.
        
        Args:
            room_id: The room identifier
            code: The new code content
            
        Returns:
            Room or None: The updated room or None if not found
        """
        room = self.get_room(room_id)
        if room:
            room.code = code
            room.updated_at = datetime.utcnow()
            self.db.commit()
            self.db.refresh(room)
        return room
    
    def increment_active_users(self, room_id: str) -> Room | None:
        """
        Increment active users count for a room.
        
        Args:
            room_id: The room identifier
            
        Returns:
            Room or None: The updated room or None if not found
        """
        room = self.get_room(room_id)
        if room:
            room.active_users = max(0, room.active_users + 1)
            self.db.commit()
            self.db.refresh(room)
        return room
    
    def decrement_active_users(self, room_id: str) -> Room | None:
        """
        Decrement active users count for a room.
        
        Args:
            room_id: The room identifier
            
        Returns:
            Room or None: The updated room or None if not found
        """
        room = self.get_room(room_id)
        if room:
            room.active_users = max(0, room.active_users - 1)
            self.db.commit()
            self.db.refresh(room)
        return room
    
    def delete_room(self, room_id: str) -> bool:
        """
        Delete a room.
        
        Args:
            room_id: The room identifier
            
        Returns:
            bool: True if deleted, False if not found
        """
        room = self.get_room(room_id)
        if room:
            self.db.delete(room)
            self.db.commit()
            return True
        return False
