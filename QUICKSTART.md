# Pair Programming IDE - Quick Start Guide

## Development Setup (5 minutes)

### Prerequisites
- Python 3.8+
- PostgreSQL (or Docker)

### Step 1: Setup Backend

```bash
cd backend

# Create virtual environment
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt

# Setup PostgreSQL (with Docker)
docker run --name pair-db -e POSTGRES_PASSWORD=password -e POSTGRES_DB=pair_programming -p 5432:5432 -d postgres:15

# Or with local PostgreSQL
createdb pair_programming

# Start backend
uvicorn app.main:app --reload --host 0.0.0.0 --port 8000
```

Backend runs at: http://localhost:8000
API Docs at: http://localhost:8000/docs

### Step 2: Setup Frontend

```bash
cd frontend

# Using Python
python -m http.server 3000

# Or using Node
npx http-server -p 3000
```

Frontend available at: http://localhost:3000

## Usage

1. Open http://localhost:3000
2. Room is created automatically
3. Copy the URL to share with your pair programmer
4. They open the URL - code syncs instantly!

## Using Docker Compose (Recommended)

```bash
# Start everything
docker-compose up

# Backend: http://localhost:8000
# Postgres: localhost:5432

# Stop
docker-compose down
```

## Testing Endpoints

### Create Room
```bash
curl -X POST http://localhost:8000/api/rooms
```

### Get Autocomplete
```bash
curl -X POST http://localhost:8000/api/autocomplete \
  -H "Content-Type: application/json" \
  -d '{"prefix":"def","language":"python"}'
```

### Health Check
```bash
curl http://localhost:8000/health
```

## Environment Variables

Create `.env` in `backend/`:
```
DATABASE_URL=postgresql://user:password@localhost:5432/pair_programming
DEBUG=True
```

## Common Issues

**WebSocket Connection Failed?**
- Check backend is running on port 8000
- Check browser console for errors
- Ensure CORS is enabled

**Database Connection Error?**
- Verify PostgreSQL is running
- Check connection string in `.env`
- Run: `psql -U user -d pair_programming -c "SELECT 1"`

**Code Not Syncing?**
- Check WebSocket connection status (green indicator)
- Refresh the page
- Check browser console for errors

## Next Steps

1. Read the full README.md
2. Explore API documentation at http://localhost:8000/docs
3. Check the code architecture in README.md
4. Deploy to production using Docker

## Need Help?

- Check README.md for detailed documentation
- Review error messages in browser console
- Check backend logs in terminal
- Check database logs: `docker logs pair-db`
