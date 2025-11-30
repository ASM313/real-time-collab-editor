# Pair Programming IDE

A production-ready real-time collaborative code editor enabling pair programming through WebSockets.

## Quick Links

- **[README.md](./README.md)** - Full documentation
- **[QUICKSTART.md](./QUICKSTART.md)** - 5-minute setup guide
- **Backend**: FastAPI + WebSockets + PostgreSQL
- **Frontend**: HTML/CSS/Vanilla JS

## Key Features

✅ Real-time code synchronization
✅ WebSocket-based communication
✅ Persistent storage with PostgreSQL
✅ Autocomplete suggestions
✅ Multi-language support
✅ User tracking
✅ No authentication required
✅ Clean, production-ready code

## Quick Start

```bash
# Backend
cd backend
python -m venv venv
source venv/bin/activate
pip install -r requirements.txt
uvicorn app.main:app --reload

# Frontend (new terminal)
cd frontend
python -m http.server 3000
```

Open http://localhost:3000 and share the room URL!

## Architecture

**Backend Layers:**
- Models: SQLAlchemy ORM (Room model)
- Schemas: Pydantic validation
- Services: RoomService, AutocompleteService
- Routers: REST endpoints
- WebSockets: Real-time synchronization
- Database: PostgreSQL

**Frontend:**
- Single-page application
- Real-time editor with line numbers
- WebSocket client
- Autocomplete suggestions
- Responsive design

## API Endpoints

```
POST   /api/rooms                    # Create room
GET    /api/rooms/{room_id}          # Get room details
POST   /api/autocomplete             # Get suggestions
WS     /ws/{room_id}                 # WebSocket connection
```

## Tech Stack

- **Backend**: Python 3.11, FastAPI, SQLAlchemy, PostgreSQL
- **Frontend**: HTML5, CSS3, Vanilla JavaScript
- **Infrastructure**: Docker, Docker Compose
- **Protocol**: WebSockets (real-time), HTTP REST

## Database Schema

Single `rooms` table with:
- room_id (UUID)
- code (TEXT)
- created_at / updated_at (TIMESTAMP)
- active_users (INTEGER)

## Design Decisions

1. **Last-Write-Wins**: Simple sync strategy (can upgrade to CRDT)
2. **In-Memory Connections**: Fast WebSocket management
3. **No Auth**: Easy sharing and demo
4. **PostgreSQL**: Persistent room state
5. **Vanilla JS**: Lightweight frontend

## What Could Be Improved

1. **Conflict Resolution**: Implement OT or CRDT for concurrent edits
2. **Scalability**: Add Redis PubSub for multi-server
3. **Authentication**: JWT-based user identification
4. **Performance**: Delta-based updates instead of full code
5. **Features**: Syntax highlighting, undo/redo, file management
6. **Tests**: Unit and integration tests
7. **Monitoring**: Logging, metrics, alerts
8. **Security**: Rate limiting, HTTPS/WSS, input sanitization

## Production Considerations

- Use environment variables for config
- Enable CORS selectively
- Implement rate limiting
- Add proper logging and monitoring
- Use HTTPS/WSS
- Database connection pooling
- Graceful shutdown handling
- Health checks and readiness probes

See README.md for complete documentation!
