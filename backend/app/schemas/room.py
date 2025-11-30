from pydantic import BaseModel
from datetime import datetime
from typing import List, Optional


class RoomCreate(BaseModel):
    """Schema for creating a room."""
    pass


class RoomResponse(BaseModel):
    """Schema for room response."""
    room_id: str
    code: str
    created_at: datetime
    updated_at: datetime
    active_users: int
    
    class Config:
        from_attributes = True


class CodeUpdate(BaseModel):
    """Schema for code update via WebSocket."""
    action: str  # "update", "join", "leave"
    room_id: str
    code: Optional[str] = None
    user_id: Optional[str] = None
    position: Optional[int] = None  # For future cursor position tracking


class AutocompleteRequest(BaseModel):
    """Schema for autocomplete request."""
    prefix: str
    language: str = "python"


class AutocompleteResponse(BaseModel):
    """Schema for autocomplete response."""
    suggestions: List[str]
