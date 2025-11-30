from typing import Dict, Set
from fastapi import WebSocket
import json
import logging

logger = logging.getLogger(__name__)


class ConnectionManager:
    """Manages WebSocket connections for each room."""
    
    def __init__(self):
        # Dictionary mapping room_id to set of active connections
        self.active_connections: Dict[str, Set[WebSocket]] = {}
    
    async def connect(self, room_id: str, websocket: WebSocket) -> None:
        """
        Register a new WebSocket connection for a room.
        
        Args:
            room_id: The room identifier
            websocket: The WebSocket connection
        """
        await websocket.accept()
        
        if room_id not in self.active_connections:
            self.active_connections[room_id] = set()
        
        self.active_connections[room_id].add(websocket)
        logger.info(f"User connected to room {room_id}. Active connections: {len(self.active_connections[room_id])}")
    
    async def disconnect(self, room_id: str, websocket: WebSocket) -> None:
        """
        Unregister a WebSocket connection from a room.
        
        Args:
            room_id: The room identifier
            websocket: The WebSocket connection
        """
        if room_id in self.active_connections:
            self.active_connections[room_id].discard(websocket)
            
            # Clean up empty rooms
            if not self.active_connections[room_id]:
                del self.active_connections[room_id]
            
            logger.info(f"User disconnected from room {room_id}")
    
    async def broadcast(self, room_id: str, message: dict) -> None:
        """
        Broadcast a message to all connections in a room.
        
        Args:
            room_id: The room identifier
            message: The message to broadcast (will be JSON serialized)
        """
        if room_id in self.active_connections:
            disconnected = []
            for connection in self.active_connections[room_id]:
                try:
                    await connection.send_json(message)
                except Exception as e:
                    logger.error(f"Error broadcasting to connection: {e}")
                    disconnected.append(connection)
            
            # Remove failed connections
            for connection in disconnected:
                await self.disconnect(room_id, connection)
    
    async def send_personal(self, websocket: WebSocket, message: dict) -> None:
        """
        Send a message to a specific connection.
        
        Args:
            websocket: The WebSocket connection
            message: The message to send
        """
        try:
            await websocket.send_json(message)
        except Exception as e:
            logger.error(f"Error sending personal message: {e}")
    
    def get_active_users_count(self, room_id: str) -> int:
        """
        Get the number of active connections in a room.
        
        Args:
            room_id: The room identifier
            
        Returns:
            int: Number of active connections
        """
        return len(self.active_connections.get(room_id, set()))


# Global connection manager instance
manager = ConnectionManager()
