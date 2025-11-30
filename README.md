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

### 1. Backend Setup

**Clone and navigate to the backend:**
```bash
cd backend
```

**Create a virtual environment:**
```bash
python -m venv venv

# On Windows
venv\Scripts\activate

# On macOS/Linux
source venv/bin/activate
```

**Install dependencies:**
```bash
pip install -r requirements.txt
```

**Setup PostgreSQL:**

Option A - Using Docker:
```bash
docker run --name postgres-pair-dev -e POSTGRES_PASSWORD=password -e POSTGRES_DB=pair_programming -p 5432:5432 -d postgres:15
```

Option B - Using local PostgreSQL:
```bash
createdb pair_programming
```

**Configure environment variables:**
```bash
cp .env.example .env
# Edit .env with your database URL
```

**Initialize database:**
```bash
# Database tables will be created automatically on app startup
```

**Run the backend:**
```bash
# Using uvicorn directly
uvicorn app.main:app --reload --host 0.0.0.0 --port 8000

# Or using Python module
python -m uvicorn app.main:app --reload --host 0.0.0.0 --port 8000
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

## 🛡️ Design Decisions

### 1. Last-Write-Wins Strategy
- **Reason**: Simpler than Operational Transformation (OT) or CRDT
- **Trade-off**: Potential loss of concurrent edits, but acceptable for pair programming where developers typically work sequentially
- **Future**: Could be improved with proper conflict resolution

### 2. In-Memory Connection Management
- **Reason**: Lightweight and fast for real-time updates
- **Trade-off**: Connections lost on server restart; no distributed deployment support
- **Future**: Redis PubSub for multi-server deployment

### 3. No Authentication
- **Reason**: Simplicity and ease of use
- **Trade-off**: No user identification or audit trail
- **Future**: Add JWT-based authentication and rate limiting

### 4. PostgreSQL for Persistence
- **Reason**: Reliable persistence of room state
- **Trade-off**: Added complexity vs in-memory storage
- **Future**: Could use Redis for faster performance

### 5. Vanilla JavaScript Frontend
- **Reason**: No build process, lightweight, easy to understand
- **Trade-off**: Limited to ES6+ features, no component system
- **Future**: Could migrate to React/Vue for complex features

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

## 📈 Performance Considerations

### Current Bottlenecks
1. Broadcasting sends full code to all clients (could optimize with delta updates)
2. No message batching (could batch updates in time windows)
3. No compression (could compress large code files)

### Optimization Opportunities
1. Implement delta/diff-based updates
2. Add message batching and throttling
3. Compress WebSocket messages
4. Add caching for frequently accessed rooms
5. Implement room expiration for cleanup

## 🔐 Security Considerations

### Current Limitations
- No authentication or authorization
- No rate limiting
- No input validation beyond Pydantic schemas
- No HTTPS/WSS in development

### Production Recommendations
1. Add JWT authentication
2. Implement rate limiting (sliding window)
3. Add CORS whitelist
4. Use HTTPS/WSS
5. Sanitize input to prevent code injection
6. Add API key management
7. Implement audit logging
8. Add DDoS protection

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

## 📝 Future Enhancements

### Short Term (MVP+)
- [ ] Persistent connection retry logic
- [ ] Message history persistence
- [ ] User identity with colors/cursors
- [ ] Syntax highlighting (Highlight.js)
- [ ] Code execution sandbox integration

### Medium Term
- [ ] Multi-language support in UI
- [ ] File upload/download
- [ ] Collaborative cursor tracking
- [ ] Code commenting and annotations
- [ ] Real-time presence indicators
- [ ] Undo/Redo with history

### Long Term
- [ ] Operational Transform (OT) or CRDT for conflict resolution
- [ ] Database replication for high availability
- [ ] Redis for distributed deployments
- [ ] Mobile native apps
- [ ] Video/Audio chat integration
- [ ] AI-powered code suggestions
- [ ] Version control integration

## 🐛 Known Limitations

1. **Concurrent Edits**: Last-write-wins may lose edits if two users type simultaneously
2. **Large Code Files**: Performance degrades with very large files (10k+ lines)
3. **No Undo/Redo**: Changes are immediately persisted
4. **Single Server**: No load balancing or failover
5. **Memory Usage**: All active connections stored in memory
6. **No Room Cleanup**: Empty rooms persist indefinitely

## 🚨 Troubleshooting

### WebSocket Connection Fails
1. Check backend is running: `http://localhost:8000/health`
2. Check CORS is enabled (should be by default)
3. Check firewall allows port 8000
4. Browser console for detailed error messages

### Database Connection Error
1. Verify PostgreSQL is running
2. Check database URL in `.env`
3. Verify credentials
4. Run: `psql -U user -d pair_programming -c "SELECT 1"`

### Code Not Syncing
1. Check WebSocket is connected (green indicator)
2. Check browser console for errors
3. Refresh page to reconnect
4. Check backend logs for issues

### Autocomplete Not Working
1. Check backend `/api/autocomplete` endpoint responds
2. Verify prefix is being sent
3. Check selected language is correct

## 📄 Project Structure

```
pair-programming-app/
├── backend/
│   ├── app/
│   │   ├── models/
│   │   │   ├── __init__.py
│   │   │   └── room.py
│   │   ├── schemas/
│   │   │   ├── __init__.py
│   │   │   └── room.py
│   │   ├── services/
│   │   │   ├── __init__.py
│   │   │   ├── room_service.py
│   │   │   └── autocomplete_service.py
│   │   ├── routers/
│   │   │   ├── __init__.py
│   │   │   ├── rooms.py
│   │   │   └── autocomplete.py
│   │   ├── websockets/
│   │   │   ├── __init__.py
│   │   │   └── connection_manager.py
│   │   ├── db/
│   │   │   ├── __init__.py
│   │   │   ├── base.py
│   │   │   └── database.py
│   │   ├── __init__.py
│   │   ├── config.py
│   │   └── main.py
│   ├── requirements.txt
│   ├── .env.example
│   └── .gitignore
├── frontend/
│   ├── index.html
│   ├── styles.css
│   └── app.js
└── README.md
```

## 🤝 Contributing

Contributions welcome! Areas for improvement:
- Better error handling and user feedback
- Enhanced autocomplete with more languages
- Performance optimizations
- Unit and integration tests
- Docker support
- CI/CD pipeline

## 📄 License

MIT License - feel free to use this project for learning and development.

## 🙏 Acknowledgments

- FastAPI documentation and community
- WebSocket protocol specification
- PostgreSQL documentation
- CSS design inspiration from modern web applications

## 📞 Support

For issues, questions, or suggestions:
1. Check this README first
2. Review GitHub Issues (if applicable)
3. Check browser console for errors
4. Check backend logs with `--log-level debug`

---

**Happy Coding! 👨‍💻👩‍💻**
