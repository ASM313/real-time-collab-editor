"""
Example usage and API test file.
Demonstrates how to interact with the API.
"""

import requests
import json
from typing import Dict

BASE_URL = "http://localhost:8000/api"

def create_room() -> Dict:
    """Create a new room."""
    response = requests.post(f"{BASE_URL}/rooms")
    print(f"Create Room: {response.status_code}")
    print(json.dumps(response.json(), indent=2))
    return response.json()

def get_room(room_id: str) -> Dict:
    """Get room details."""
    response = requests.get(f"{BASE_URL}/rooms/{room_id}")
    print(f"Get Room: {response.status_code}")
    print(json.dumps(response.json(), indent=2))
    return response.json()

def get_autocomplete(prefix: str, language: str = "python") -> Dict:
    """Get autocomplete suggestions."""
    payload = {"prefix": prefix, "language": language}
    response = requests.post(
        f"{BASE_URL}/autocomplete",
        json=payload,
        headers={"Content-Type": "application/json"}
    )
    print(f"Autocomplete '{prefix}': {response.status_code}")
    print(json.dumps(response.json(), indent=2))
    return response.json()

if __name__ == "__main__":
    print("=" * 50)
    print("Pair Programming API - Example Usage")
    print("=" * 50)
    
    # Create a room
    print("\n1. Creating a room...")
    room_data = create_room()
    room_id = room_data["room_id"]
    
    # Get room details
    print("\n2. Getting room details...")
    get_room(room_id)
    
    # Get autocomplete suggestions
    print("\n3. Getting autocomplete suggestions...")
    print("\nPython suggestions for 'def':")
    get_autocomplete("def", "python")
    
    print("\nJavaScript suggestions for 'async':")
    get_autocomplete("async", "javascript")
    
    print("\n" + "=" * 50)
    print(f"Room ID: {room_id}")
    print(f"Frontend URL: http://localhost:3000?room={room_id}")
    print("=" * 50)
