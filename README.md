# Pair Programming IDE

A real-time collaborative code editor that allows two or more developers to code together in the same room. Built with FastAPI backend and vanilla JavaScript frontend.

![Architecture](https://img.shields.io/badge/Backend-FastAPI-brightgreen) ![WebSocket](https://img.shields.io/badge/Protocol-WebSocket-blue) ![Database](https://img.shields.io/badge/Database-PostgreSQL-336791)

## 🚀 Features

- **Real-Time Collaboration**: See your pair programmer's changes instantly
- **Room-Based Architecture**: Create rooms for different projects/sessions
- **WebSocket Integration**: Bi-directional real-time communication
- **Code Synchronization**: Last-write-wins strategy for code state
- **Autocomplete Suggestions**: Language-aware code completions (Python, JavaScript)
- **User Tracking**: Know how many developers are in your room
- **No Authentication Required**: Simple URL sharing for easy access
- **Responsive UI**: Works on desktop and tablet devices

## 🏗️ Architecture

### Backend Structure
```
backend/
├── app/
│   ├── models/          # Database models (Room)
│   ├── schemas/         # Pydantic schemas for validation
│   ├── routers/         # API endpoints (rooms, autocomplete)
│   ├── services/        # Business logic (RoomService, AutocompleteService)
│   ├── websockets/      # WebSocket connection manager
│   ├── db/              # Database configuration and sessions
│   ├── config.py        # Configuration settings
│   └── main.py          # FastAPI application and WebSocket endpoints
├── requirements.txt     # Python dependencies
└── .env.example         # Environment variables template
```

### Frontend Structure
```
frontend/
├── index.html           # Main HTML structure
├── styles.css           # Styling and responsive design
└── app.js              # JavaScript logic for UI and WebSocket communication
```

## 🔧 Technology Stack

### Backend
- **FastAPI**: Modern Python web framework with automatic API documentation
- **WebSockets**: Real-time bidirectional communication protocol
- **SQLAlchemy**: ORM for database operations
- **PostgreSQL**: Relational database for storing room and code state
- **Pydantic**: Data validation and serialization

### Frontend
- **HTML5**: Semantic markup
- **CSS3**: Modern styling with CSS variables and flexbox
- **Vanilla JavaScript**: No framework dependencies for lightweight implementation

## 📋 Prerequisites

- Python 3.8+
- PostgreSQL 12+ (or use SQLite for development)
- Node.js (optional, for frontend tooling)

## 🚀 Getting Started

**Configure environment variables:**
```bash
cp .env.example .env
# Edit .env with your database URL
```

**Using Docker:**
```bash
docker compose up --build -d
```


Backend will be available at `http://localhost:8000`
API docs available at `http://localhost:8000/docs`

### 2. Frontend Setup

**Navigate to the frontend directory:**
```bash
cd frontend
```

**Start a local development server:**

Option A - Using Python:
```bash
# Python 3.8+
python -m http.server 3000
```

Option B - Using Node.js:
```bash
npx http-server -p 3000
```

Option C - Using any static server:
```bash
# Any static file server will work
```

**Access the application:**
Open `http://localhost:3000` in your browser.

## 📖 API Endpoints

### REST Endpoints

**Create a new room:**
```
POST /api/rooms
Response: { "room_id": "uuid", "code": "", "created_at": "...", "updated_at": "...", "active_users": 0 }
```

**Get room details:**
```
GET /api/rooms/{room_id}
Response: { "room_id": "uuid", "code": "...", "created_at": "...", "updated_at": "...", "active_users": 1 }
```

**Get autocomplete suggestions:**
```
POST /api/autocomplete
Body: { "prefix": "def", "language": "python" }
Response: { "suggestions": ["def function_name():", "def __init__(self):"] }
```

### WebSocket Endpoint

**Connect to room:**
```
WS /ws/{room_id}
```

**Message Types:**

1. **Code Update** (User → Server → All Users):
```json
{
  "action": "update",
  "room_id": "uuid",
  "code": "print('hello')",
  "user_id": "user_123"
}
```

2. **Cursor Position** (User → Server → All Users):
```json
{
  "action": "cursor_position",
  "room_id": "uuid",
  "user_id": "user_123",
  "position": 42
}
```

3. **Server Messages to Clients:**
```json
{
  "type": "sync",
  "code": "...",
  "active_users": 2
}
```

```json
{
  "type": "code_update",
  "code": "...",
  "user_id": "user_123"
}
```

```json
{
  "type": "user_joined",
  "active_users": 2
}
```

```json
{
  "type": "user_left",
  "active_users": 1
}
```

## 📊 Database Schema

### Rooms Table
```sql
CREATE TABLE rooms (
    room_id VARCHAR(36) PRIMARY KEY,
    code TEXT NOT NULL DEFAULT '',
    created_at TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
    active_users INTEGER NOT NULL DEFAULT 0
);
```

## 🔄 Data Synchronization Flow

1. **User A** types code and presses a key
2. **User A's frontend** sends code via WebSocket
3. **Backend** receives message and:
   - Updates room in database
   - Broadcasts update to all connected clients
4. **User B's frontend** receives updated code
5. **User B's editor** is updated with new code

## 🎯 Workflow Example

1. **Create Room**: 
   - Go to `http://localhost:3000`
   - Room ID is generated automatically
   - Copy the link to share with pair programmer

2. **Share Room**:
   - Click "Copy Link" button
   - Send link to your pair programmer

3. **Join Room**:
   - Your pair programmer opens the link
   - Code is synchronized automatically
   - Both see changes in real-time

4. **Collaborate**:
   - Take turns typing
   - Use autocomplete for suggestions
   - See active user count

## 🧪 Testing

### Manual Testing with cURL

**Create a room:**
```bash
curl -X POST http://localhost:8000/api/rooms \
  -H "Content-Type: application/json"
```

**Get room details:**
```bash
curl http://localhost:8000/api/rooms/{room_id}
```

**Get autocomplete:**
```bash
curl -X POST http://localhost:8000/api/autocomplete \
  -H "Content-Type: application/json" \
  -d '{"prefix":"def","language":"python"}'
```

### WebSocket Testing with wscat
```bash
npm install -g wscat

# Connect to WebSocket
wscat -c ws://localhost:8000/ws/{room_id}

# Send message
{"action": "update", "room_id": "...", "code": "print('hello')", "user_id": "user_1"}
```


## 🐛 Known Limitations

1. **Concurrent Edits**: Last-write-wins may lose edits if two users type simultaneously
2. **Large Code Files**: Performance degrades with very large files (10k+ lines)
3. **No Undo/Redo**: Changes are immediately persisted
4. **Single Server**: No load balancing or failover
5. **Memory Usage**: All active connections stored in memory
6. **No Room Cleanup**: Empty rooms persist indefinitely
