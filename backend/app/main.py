from fastapi import FastAPI, WebSocket, WebSocketDisconnect, Depends, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from sqlalchemy.orm import Session
import json
import logging

from app.config import settings
from app.db import engine, Base, get_db
from app.routers import rooms, autocomplete
from app.websockets.connection_manager import manager
from app.services.room_service import RoomService

# Initialize database tables
Base.metadata.create_all(bind=engine)

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Create FastAPI app
app = FastAPI(
    title=settings.app_name,
    debug=settings.debug,
    version="1.0.0"
)

# Add CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Include routers
app.include_router(rooms.router, prefix=settings.api_prefix)
app.include_router(autocomplete.router, prefix=settings.api_prefix)


@app.get("/health")
async def health_check() -> dict:
    """Health check endpoint."""
    return {"status": "healthy", "service": settings.app_name}


@app.websocket("/ws/{room_id}")
async def websocket_endpoint(room_id: str, websocket: WebSocket, db: Session = Depends(get_db)):
    """
    WebSocket endpoint for real-time code synchronization.
    
    Args:
        room_id: The room identifier
        websocket: The WebSocket connection
        db: Database session
    """
    # Connect the user and get assigned user_id and color
    user_id, color = await manager.connect(room_id, websocket)
    
    try:
        # Verify room exists
        room_service = RoomService(db)
        room = room_service.get_room(room_id)
        
        if not room:
            await websocket.send_json({
                "type": "error",
                "message": "Room not found"
            })
            await manager.disconnect(room_id, user_id)
            return
        
        # Increment active users
        room_service.increment_active_users(room_id)
        
        # Send initial code state to the new user with user info
        await websocket.send_json({
            "type": "sync",
            "code": room.code,
            "active_users": manager.get_active_users_count(room_id),
            "user_id": user_id,
            "color": color,
            "users": manager.get_all_users(room_id)
        })
        
        # Notify others that a user joined with their color
        await manager.broadcast(room_id, {
            "type": "user_joined",
            "active_users": manager.get_active_users_count(room_id),
            "user_id": user_id,
            "color": color,
            "users": manager.get_all_users(room_id)
        })
        
        logger.info(f"User joined room {room_id}")
        
        # Listen for messages
        while True:
            data = await websocket.receive_text()
            message = json.loads(data)
            
            action = message.get("action")
            
            if action == "update":
                # Update code in database and broadcast to others
                new_code = message.get("code", "")
                room_service.update_code(room_id, new_code)
                
                # Broadcast the update to all clients in the room
                await manager.broadcast(room_id, {
                    "type": "code_update",
                    "code": new_code,
                    "user_id": user_id,
                    "color": color
                })
            
            elif action == "cursor_position":
                # Broadcast cursor position with user color
                await manager.broadcast(room_id, {
                    "type": "cursor_update",
                    "user_id": user_id,
                    "color": color,
                    "position": message.get("position"),
                    "line": message.get("line")
                })
            
            else:
                logger.warning(f"Unknown action: {action}")
    
    except WebSocketDisconnect:
        await manager.disconnect(room_id, user_id)
        
        # Decrement active users
        room_service = RoomService(db)
        room_service.decrement_active_users(room_id)
        
        # Notify remaining users
        active_count = manager.get_active_users_count(room_id)
        if active_count > 0:
            await manager.broadcast(room_id, {
                "type": "user_left",
                "active_users": active_count,
                "user_id": user_id,
                "users": manager.get_all_users(room_id)
            })
        else:
            logger.info(f"Room {room_id} is now empty")
        
        logger.info(f"User disconnected from room {room_id}")
    
    except Exception as e:
        logger.error(f"WebSocket error in room {room_id}: {e}")
        await manager.disconnect(room_id, websocket)


@app.on_event("startup")
async def startup_event():
    """Startup event."""
    logger.info(f"Starting {settings.app_name}")
    logger.info(f"Database URL: {settings.database_url[:30]}...")


@app.on_event("shutdown")
async def shutdown_event():
    """Shutdown event."""
    logger.info(f"Shutting down {settings.app_name}")
