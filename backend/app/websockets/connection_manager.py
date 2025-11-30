from typing import Dict, Set, Tuple
from fastapi import WebSocket
import json
import logging
import uuid

logger = logging.getLogger(__name__)

# Color palette for different users (vibrant colors)
COLOR_PALETTE = [
    "#FF6B6B",  # Red
    "#4ECDC4",  # Teal
    "#45B7D1",  # Blue
    "#FFA07A",  # Salmon
    "#98D8C8",  # Mint
    "#F7DC6F",  # Yellow
    "#BB8FCE",  # Purple
    "#85C1E2",  # Sky Blue
    "#F8B88B",  # Peach
    "#A8E6CF",  # Light Green
]


class UserConnection:
    """Represents a user connection with ID and color."""
    def __init__(self, websocket: WebSocket, user_id: str = None, color: str = None):
        self.websocket = websocket
        self.user_id = user_id or str(uuid.uuid4())[:8]  # Generate short ID
        self.color = color or "#808080"  # Default gray
        self.cursor_position = 0


class ConnectionManager:
    """Manages WebSocket connections for each room with user tracking."""
    
    def __init__(self):
        # Dictionary mapping room_id to dict of user_id -> UserConnection
        self.active_connections: Dict[str, Dict[str, UserConnection]] = {}
        self.user_colors: Dict[str, int] = {}  # Track color index per room
    
    async def connect(self, room_id: str, websocket: WebSocket) -> Tuple[str, str]:
        """
        Register a new WebSocket connection for a room.
        
        Args:
            room_id: The room identifier
            websocket: The WebSocket connection
            
        Returns:
            Tuple[str, str]: (user_id, color) assigned to this connection
        """
        await websocket.accept()
        
        if room_id not in self.active_connections:
            self.active_connections[room_id] = {}
            self.user_colors[room_id] = 0
        
        # Assign color based on connection order
        color_index = self.user_colors[room_id] % len(COLOR_PALETTE)
        color = COLOR_PALETTE[color_index]
        self.user_colors[room_id] += 1
        
        # Create user connection
        user_connection = UserConnection(websocket, color=color)
        self.active_connections[room_id][user_connection.user_id] = user_connection
        
        logger.info(f"User {user_connection.user_id} connected to room {room_id} with color {color}. Active users: {len(self.active_connections[room_id])}")
        
        return user_connection.user_id, color
    
    async def disconnect(self, room_id: str, user_id: str) -> None:
        """
        Unregister a WebSocket connection from a room.
        
        Args:
            room_id: The room identifier
            user_id: The user identifier
        """
        if room_id in self.active_connections:
            if user_id in self.active_connections[room_id]:
                del self.active_connections[room_id][user_id]
            
            # Clean up empty rooms
            if not self.active_connections[room_id]:
                del self.active_connections[room_id]
                if room_id in self.user_colors:
                    del self.user_colors[room_id]
            
            logger.info(f"User {user_id} disconnected from room {room_id}")
    
    async def broadcast(self, room_id: str, message: dict) -> None:
        """
        Broadcast a message to all connections in a room.
        
        Args:
            room_id: The room identifier
            message: The message to broadcast (will be JSON serialized)
        """
        if room_id in self.active_connections:
            disconnected = []
            for user_id, user_conn in list(self.active_connections[room_id].items()):
                try:
                    await user_conn.websocket.send_json(message)
                except Exception as e:
                    logger.error(f"Error broadcasting to connection {user_id}: {e}")
                    disconnected.append(user_id)
            
            # Remove failed connections
            for user_id in disconnected:
                await self.disconnect(room_id, user_id)
    
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
    
    def get_user_info(self, room_id: str, user_id: str) -> dict:
        """
        Get user information (ID and color).
        
        Args:
            room_id: The room identifier
            user_id: The user identifier
            
        Returns:
            dict: User information with id and color
        """
        if room_id in self.active_connections and user_id in self.active_connections[room_id]:
            user_conn = self.active_connections[room_id][user_id]
            return {
                "user_id": user_id,
                "color": user_conn.color
            }
        return None
    
    def get_all_users(self, room_id: str) -> list:
        """
        Get all active users in a room with their colors.
        
        Args:
            room_id: The room identifier
            
        Returns:
            list: List of user info dicts
        """
        users = []
        if room_id in self.active_connections:
            for user_id, user_conn in self.active_connections[room_id].items():
                users.append({
                    "user_id": user_id,
                    "color": user_conn.color
                })
        return users
    
    def get_active_users_count(self, room_id: str) -> int:
        """
        Get the number of active connections in a room.
        
        Args:
            room_id: The room identifier
            
        Returns:
            int: Number of active connections
        """
        return len(self.active_connections.get(room_id, {}))


# Global connection manager instance
manager = ConnectionManager()
