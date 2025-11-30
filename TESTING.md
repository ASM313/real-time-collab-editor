# Testing Guide - Pair Programming IDE

## ✅ Automated Testing

### Setup for Testing

```bash
cd backend
pip install pytest pytest-asyncio httpx
```

### Test Files to Create

Create `backend/test_api.py`:

```python
import pytest
from fastapi.testclient import TestClient
from app.main import app

client = TestClient(app)

def test_health_check():
    """Test health check endpoint"""
    response = client.get("/health")
    assert response.status_code == 200
    assert response.json()["status"] == "healthy"

def test_create_room():
    """Test room creation"""
    response = client.post("/api/rooms")
    assert response.status_code == 201
    assert "room_id" in response.json()
    assert response.json()["active_users"] == 0

def test_get_room():
    """Test getting room details"""
    # Create a room
    create_response = client.post("/api/rooms")
    room_id = create_response.json()["room_id"]
    
    # Get the room
    response = client.get(f"/api/rooms/{room_id}")
    assert response.status_code == 200
    assert response.json()["room_id"] == room_id

def test_autocomplete():
    """Test autocomplete endpoint"""
    response = client.post(
        "/api/autocomplete",
        json={"prefix": "def", "language": "python"}
    )
    assert response.status_code == 200
    assert "suggestions" in response.json()
    assert isinstance(response.json()["suggestions"], list)

def test_autocomplete_javascript():
    """Test JavaScript autocomplete"""
    response = client.post(
        "/api/autocomplete",
        json={"prefix": "async", "language": "javascript"}
    )
    assert response.status_code == 200
    suggestions = response.json()["suggestions"]
    assert len(suggestions) > 0
```

### Run Tests

```bash
pytest backend/test_api.py -v
```

---

## 🧪 Manual Testing Scenarios

### Scenario 1: Create and Access Room

**Steps:**
1. Make API call to create room
2. Verify room_id is returned
3. Access frontend with room_id parameter
4. Verify empty code editor loads

**Expected Result:** ✅ Room created and accessible

**Test Command:**
```bash
curl -X POST http://localhost:8000/api/rooms | jq .room_id
# Use room_id in: http://localhost:3000?room={room_id}
```

---

### Scenario 2: Real-Time Sync - Two Users

**Steps:**
1. Open http://localhost:3000 in Browser A
2. Copy room URL
3. Open same URL in Browser B
4. Type code in Browser A
5. Verify code appears instantly in Browser B
6. Type different code in Browser B
7. Verify code updates in Browser A

**Expected Result:** ✅ Real-time synchronization works

**WebSocket Connection Indicators:**
- Green indicator next to "Connection"
- Message shows "Connected"
- Sync status updates when code changes

---

### Scenario 3: Multiple Users Join/Leave

**Steps:**
1. Create room in Browser A
2. Join with Browser B - see "2 users"
3. Join with Browser C - see "3 users"
4. Close Browser B - see "2 users"
5. Close Browser C - see "1 user"

**Expected Result:** ✅ Active user count accurate

**Visual Verification:**
- Top right shows "2 users"
- Status panel shows "Connected Users: 2"
- Broadcast message logged in console

---

### Scenario 4: Code Persistence

**Steps:**
1. Create room, add code: `print("hello")`
2. Close and reopen room URL
3. Verify code is still there
4. New user joins - sees same code

**Expected Result:** ✅ Code persisted in database

**Verification:**
```bash
# Check database directly
psql -U user -d pair_programming -c "SELECT code FROM rooms WHERE room_id='xxx';"
```

---

### Scenario 5: Autocomplete Suggestions

**Steps:**
1. Type "def" in editor
2. Go to Suggestions tab
3. Click "Get Suggestions"
4. See Python suggestions
5. Change language to JavaScript
6. Type "async" and get suggestions
7. Click suggestion - code inserts

**Expected Result:** ✅ Suggestions work for both languages

**Test Command:**
```bash
curl -X POST http://localhost:8000/api/autocomplete \
  -H "Content-Type: application/json" \
  -d '{"prefix":"def","language":"python"}' | jq .
```

---

### Scenario 6: Error Handling

**Test Missing Room:**
```bash
curl http://localhost:8000/api/rooms/invalid-id
# Expected: 404 error
```

**Test Invalid Autocomplete:**
```bash
curl -X POST http://localhost:8000/api/autocomplete \
  -H "Content-Type: application/json" \
  -d '{"prefix":"","language":"python"}'
# Expected: Empty suggestions list
```

**WebSocket Disconnect:**
1. Connect to room
2. Disconnect backend
3. See reconnection attempt in frontend
4. Restart backend
5. Should reconnect automatically

---

### Scenario 7: Browser Compatibility

**Test Browsers:**
- ✅ Chrome/Chromium 90+
- ✅ Firefox 88+
- ✅ Safari 14+
- ✅ Edge 90+
- ✅ Opera 76+

**Test on Mobile:**
- ✅ iPhone Safari
- ✅ Android Chrome
- ✅ Tablet (iPad/Android)

---

### Scenario 8: Large Code Files

**Test Performance:**
1. Paste 1000 lines of code
2. Verify editor still responsive
3. Check line numbers update
4. Verify sync is instant
5. Switch tabs without lag

**Expected:** Editor remains responsive

---

### Scenario 9: Rapid Typing

**Steps:**
1. Type rapidly in Browser A
2. Monitor sync status
3. Verify no lag in Browser B
4. Check that all text appears

**Expected:** All text synced, no loss

---

### Scenario 10: Connection Recovery

**Steps:**
1. Open room in both browsers
2. Disconnect internet (or kill backend)
3. Type in disconnected browser
4. Reconnect internet/backend
5. Verify code syncs

**Expected:** Automatic reconnection and sync

---

## 🔍 Backend Testing with cURL

### Health Check
```bash
curl http://localhost:8000/health
```

### Create Multiple Rooms
```bash
for i in {1..5}; do
  curl -X POST http://localhost:8000/api/rooms | jq '.room_id'
done
```

### Get Room Status
```bash
curl http://localhost:8000/api/rooms/{room_id}
```

### Autocomplete All Languages
```bash
# Python
curl -X POST http://localhost:8000/api/autocomplete \
  -H "Content-Type: application/json" \
  -d '{"prefix":"for","language":"python"}'

# JavaScript
curl -X POST http://localhost:8000/api/autocomplete \
  -H "Content-Type: application/json" \
  -d '{"prefix":"function","language":"javascript"}'
```

---

## 🔗 WebSocket Testing with wscat

### Install wscat
```bash
npm install -g wscat
```

### Connect to WebSocket
```bash
wscat -c ws://localhost:8000/ws/{room_id}
```

### Send Code Update
```json
{
  "action": "update",
  "room_id": "xxx",
  "code": "print('hello world')",
  "user_id": "test_user_1"
}
```

### Send Cursor Position
```json
{
  "action": "cursor_position",
  "room_id": "xxx",
  "user_id": "test_user_1",
  "position": 42
}
```

### Expected Messages from Server
```json
{"type": "sync", "code": "", "active_users": 1}
{"type": "code_update", "code": "...", "user_id": "test_user_1"}
{"type": "user_joined", "active_users": 2}
{"type": "user_left", "active_users": 1}
```

---

## 📊 Load Testing

### Using Apache Bench
```bash
ab -n 1000 -c 10 http://localhost:8000/health
```

### Using wrk
```bash
wrk -t12 -c400 -d30s http://localhost:8000/health
```

### WebSocket Load Test
```bash
# Test 100 concurrent connections
for i in {1..100}; do
  wscat -c ws://localhost:8000/ws/{room_id} &
done
```

---

## 🔐 Security Testing

### SQL Injection Test
```bash
curl "http://localhost:8000/api/rooms/'; DROP TABLE rooms; --"
# Expected: 404 or handled error
```

### XSS Test
```bash
# Send code with script tags
curl -X POST http://localhost:8000/api/rooms \
  -d 'code=<script>alert("xss")</script>'
# Expected: Script not executed in other clients
```

### Rate Limit Test
```bash
# Send 100 requests rapidly
for i in {1..100}; do
  curl http://localhost:8000/api/rooms &
done
```

---

## 📈 Performance Metrics

### Measure WebSocket Latency
1. Send message with timestamp
2. Measure round-trip time
3. Expected: <100ms per update

### Measure Database Query Time
```bash
# Add timing to backend logs
# Expected: <5ms per query
```

### Measure Memory Usage
```bash
# Monitor with: docker stats
# Per connection: ~10KB
```

---

## ✅ Test Checklist

- [ ] Health check passes
- [ ] Room creation works
- [ ] Room retrieval works
- [ ] WebSocket connection works
- [ ] Code sync works (2 users)
- [ ] Code sync works (3+ users)
- [ ] User count updates correctly
- [ ] Code persists in database
- [ ] Autocomplete returns suggestions
- [ ] Both languages work
- [ ] Connection recovery works
- [ ] Large files perform well
- [ ] Error handling works
- [ ] Browser compatibility verified
- [ ] Mobile responsiveness verified
- [ ] No memory leaks
- [ ] No message loss
- [ ] Rate limiting appropriate
- [ ] Security checks pass

---

## 🚀 Continuous Integration

### GitHub Actions Example

Create `.github/workflows/test.yml`:

```yaml
name: Tests

on: [push, pull_request]

jobs:
  test:
    runs-on: ubuntu-latest
    services:
      postgres:
        image: postgres:15
        env:
          POSTGRES_DB: pair_programming
          POSTGRES_PASSWORD: password
        options: >-
          --health-cmd pg_isready
          --health-interval 10s
          --health-timeout 5s
          --health-retries 5
        ports:
          - 5432:5432

    steps:
      - uses: actions/checkout@v2
      - uses: actions/setup-python@v2
        with:
          python-version: 3.11
      
      - name: Install dependencies
        run: |
          cd backend
          pip install -r requirements.txt
          pip install pytest pytest-asyncio httpx
      
      - name: Run tests
        run: cd backend && pytest test_api.py -v
```

---

## 📞 Debugging Tips

### Enable Debug Logging
```bash
# Backend
uvicorn app.main:app --reload --log-level debug

# Frontend
Open browser console (F12)
```

### Check Database
```bash
psql -U user -d pair_programming
SELECT * FROM rooms;
SELECT * FROM rooms WHERE room_id='xxx';
```

### Monitor WebSocket Traffic
```bash
# Browser DevTools → Network → WS
# Shows all WebSocket messages in real-time
```

### Check Connections
```bash
# Backend logs
# "User connected to room"
# "User disconnected from room"
```

---

Happy Testing! 🧪
