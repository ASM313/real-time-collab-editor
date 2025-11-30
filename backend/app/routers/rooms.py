from fastapi import APIRouter, HTTPException, Depends
from sqlalchemy.orm import Session
from uuid import uuid4
from app.schemas.room import RoomCreate, RoomResponse
from app.services.room_service import RoomService
from app.db import get_db

router = APIRouter(prefix="/rooms", tags=["rooms"])


@router.post("", response_model=RoomResponse, status_code=201)
async def create_room(
    room_create: RoomCreate,
    db: Session = Depends(get_db)
) -> RoomResponse:
    """
    Create a new room for pair programming.
    
    Returns:
        RoomResponse: Room details including room_id
    """
    room_service = RoomService(db)
    room_id = str(uuid4())
    room = room_service.create_room(room_id)
    return room


@router.get("/{room_id}", response_model=RoomResponse)
async def get_room(
    room_id: str,
    db: Session = Depends(get_db)
) -> RoomResponse:
    """
    Get room details by room_id.
    
    Args:
        room_id: The room identifier
        
    Returns:
        RoomResponse: Room details
        
    Raises:
        HTTPException: If room not found
    """
    room_service = RoomService(db)
    room = room_service.get_room(room_id)
    
    if not room:
        raise HTTPException(status_code=404, detail="Room not found")
    
    return room


@router.delete("/{room_id}", status_code=204)
async def delete_room(
    room_id: str,
    db: Session = Depends(get_db)
) -> None:
    """
    Delete a room.
    
    Args:
        room_id: The room identifier
    """
    room_service = RoomService(db)
    room_service.delete_room(room_id)
