// Configuration
const API_BASE_URL = 'http://localhost:8000/api';
const WS_BASE_URL = 'ws://localhost:8000';

// Global variables
let roomId = null;
let ws = null;
let currentLanguage = 'python';
let isConnected = false;
let currentUserId = null;
let currentUserColor = null;
let remoteUsers = {};  // Track remote users and their cursors
let remoteCursors = {};  // Track cursor elements by user_id

// Initialize app on load
document.addEventListener('DOMContentLoaded', () => {
    initializeApp();
});

/**
 * Initialize the application
 */
async function initializeApp() {
    // Check if joining existing room
    const urlParams = new URLSearchParams(window.location.search);
    roomId = urlParams.get('room');

    if (roomId) {
        // Join existing room directly
        await joinRoom(roomId);
        showEditor();
    } else {
        // Show landing screen with options
        showLandingScreen();
    }

    // Setup event listeners
    setupEventListeners();
}

/**
 * Show landing screen
 */
function showLandingScreen() {
    document.getElementById('landing-screen').style.display = 'flex';
    document.getElementById('header').style.display = 'none';
    document.getElementById('main-content').style.display = 'none';
    document.getElementById('footer').style.display = 'none';
}

/**
 * Show editor
 */
function showEditor() {
    document.getElementById('landing-screen').style.display = 'none';
    document.getElementById('header').style.display = 'block';
    document.getElementById('main-content').style.display = 'flex';
    document.getElementById('footer').style.display = 'block';
    updateLineNumbers();
}

/**
 * Create room from landing screen
 */
async function landingCreateRoom() {
    try {
        const response = await fetch(`${API_BASE_URL}/rooms`, {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
            },
            body: '{}'
        });

        if (!response.ok) {
            throw new Error(`Failed to create room: ${response.statusText}`);
        }

        const data = await response.json();
        roomId = data.room_id;

        // Update URL
        window.history.pushState({}, '', `?room=${roomId}`);

        // Connect WebSocket
        connectWebSocket();
        showEditor();

        // Update UI
        document.getElementById('room-display').textContent = `Room: ${roomId.substring(0, 8)}...`;

        console.log('Room created:', roomId);
    } catch (error) {
        console.error('Error creating room:', error);
        alert('Failed to create room. Please try again.');
    }
}

/**
 * Join room from landing screen
 */
async function landingJoinRoom() {
    const input = document.getElementById('room-input').value.trim();
    
    if (!input) {
        alert('Please enter a room ID or paste a URL');
        return;
    }

    // Extract room ID from URL or use directly
    let roomToJoin = input;
    try {
        const url = new URL(input);
        roomToJoin = url.searchParams.get('room');
        if (!roomToJoin) {
            alert('Invalid URL. Please paste a valid room link or room ID.');
            return;
        }
    } catch (e) {
        // Input is not a URL, treat as room ID
        roomToJoin = input;
    }

    // Join the room
    await joinRoom(roomToJoin);
    showEditor();
}

/**
 * Create a new room
 */
async function createRoom() {
    try {
        const response = await fetch(`${API_BASE_URL}/rooms`, {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
            },
            body: '{}'
        });

        if (!response.ok) {
            throw new Error(`Failed to create room: ${response.statusText}`);
        }

        const data = await response.json();
        roomId = data.room_id;

        // Update UI
        document.getElementById('room-display').textContent = `Room: ${roomId.substring(0, 8)}...`;
        window.history.pushState({}, '', `?room=${roomId}`);

        // Connect WebSocket
        connectWebSocket();

        console.log('Room created:', roomId);
    } catch (error) {
        console.error('Error creating room:', error);
        showErrorMessage('Failed to create room. Please refresh and try again.');
    }
}

/**
 * Join an existing room
 */
async function joinRoom(id) {
    try {
        const response = await fetch(`${API_BASE_URL}/rooms/${id}`, {
            method: 'GET',
            headers: {
                'Content-Type': 'application/json',
            }
        });

        if (!response.ok) {
            throw new Error(`Room not found: ${response.statusText}`);
        }

        const data = await response.json();
        roomId = data.room_id;

        // Update UI
        document.getElementById('room-display').textContent = `Room: ${roomId.substring(0, 8)}...`;
        document.getElementById('code-editor').value = data.code;
        updateLineNumbers();

        // Connect WebSocket
        connectWebSocket();

        console.log('Joined room:', roomId);
    } catch (error) {
        console.error('Error joining room:', error);
        showErrorMessage('Failed to join room. The room may not exist.');
    }
}

/**
 * Connect to WebSocket
 */
function connectWebSocket() {
    if (!roomId) {
        console.error('No room ID available for WebSocket connection');
        return;
    }

    const wsUrl = `${WS_BASE_URL}/ws/${roomId}`;
    console.log('Connecting to WebSocket:', wsUrl);

    ws = new WebSocket(wsUrl);

    ws.onopen = () => {
        console.log('WebSocket connected');
        isConnected = true;
        updateConnectionStatus(true);
    };

    ws.onmessage = (event) => {
        const message = JSON.parse(event.data);
        handleWebSocketMessage(message);
    };

    ws.onerror = (error) => {
        console.error('WebSocket error:', error);
        updateConnectionStatus(false);
        showErrorMessage('WebSocket connection error. Attempting to reconnect...');
    };

    ws.onclose = () => {
        console.log('WebSocket disconnected');
        isConnected = false;
        updateConnectionStatus(false);
        
        // Attempt to reconnect after 3 seconds
        setTimeout(() => {
            console.log('Attempting to reconnect...');
            connectWebSocket();
        }, 3000);
    };
}

/**
 * Handle WebSocket messages
 */
function handleWebSocketMessage(message) {
    const { type, code, user_id, color, active_users, users } = message;

    switch (type) {
        case 'sync':
            // Initial sync when joining
            currentUserId = user_id;
            currentUserColor = color;
            document.getElementById('code-editor').value = code;
            updateLineNumbers();
            updateUserCount(active_users);
            if (users) {
                updateUsersList(users);
                remoteUsers = {};
                users.forEach(user => {
                    if (user.user_id !== currentUserId) {
                        remoteUsers[user.user_id] = user;
                    }
                });
            }
            console.log(`You joined as ${user_id} with color ${color}`);
            break;

        case 'code_update':
            // Another user updated code
            if (user_id !== currentUserId) {
                document.getElementById('code-editor').value = code;
                updateLineNumbers();
                updateSyncStatus(`Code updated by peer (${user_id})`);
            }
            break;

        case 'user_joined':
            updateUserCount(active_users);
            if (users) {
                updateUsersList(users);
                users.forEach(user => {
                    if (user.user_id !== currentUserId && !remoteUsers[user.user_id]) {
                        remoteUsers[user.user_id] = user;
                    }
                });
            }
            updateSyncStatus(`User ${user_id} joined (${active_users} active)`);
            console.log(`User joined. Active users: ${active_users}`);
            break;

        case 'user_left':
            updateUserCount(active_users);
            if (user_id in remoteUsers) {
                delete remoteUsers[user_id];
                removeRemoteCursor(user_id);
            }
            if (users) {
                updateUsersList(users);
            }
            updateSyncStatus(`User left (${active_users} active)`);
            console.log(`User left. Active users: ${active_users}`);
            break;

        case 'cursor_update':
            // Handle cursor position update
            if (user_id !== currentUserId) {
                updateRemoteCursor(user_id, color, message.position, message.line);
            }
            break;

        case 'error':
            showErrorMessage(message.message);
            break;

        default:
            console.warn('Unknown message type:', type);
    }
}

/**
 * Update remote cursor position
 */
function updateRemoteCursor(userId, color, position, line) {
    const container = document.getElementById('remote-cursors-container');
    
    // Create or update cursor element
    let cursorElement = document.getElementById(`cursor-${userId}`);
    if (!cursorElement) {
        cursorElement = document.createElement('div');
        cursorElement.id = `cursor-${userId}`;
        cursorElement.className = 'remote-cursor';
        cursorElement.style.backgroundColor = color;
        
        const label = document.createElement('div');
        label.className = 'cursor-label';
        label.style.backgroundColor = color;
        label.textContent = userId;
        cursorElement.appendChild(label);
        
        container.appendChild(cursorElement);
        remoteCursors[userId] = cursorElement;
    }
    
    // Calculate cursor position based on text content
    const editor = document.getElementById('code-editor');
    const text = editor.value;
    
    // Get line and column from position
    let currentLine = 1;
    let currentCol = 0;
    for (let i = 0; i < Math.min(position, text.length); i++) {
        if (text[i] === '\n') {
            currentLine++;
            currentCol = 0;
        } else {
            currentCol++;
        }
    }
    
    // Calculate pixel position (approximate)
    const lineHeight = 20;  // Approximate line height
    const charWidth = 8;    // Approximate character width
    
    cursorElement.style.left = (currentCol * charWidth) + 'px';
    cursorElement.style.top = ((currentLine - 1) * lineHeight + editor.offsetTop) + 'px';
}

/**
 * Remove remote cursor
 */
function removeRemoteCursor(userId) {
    const cursorElement = document.getElementById(`cursor-${userId}`);
    if (cursorElement) {
        cursorElement.remove();
        delete remoteCursors[userId];
    }
}

/**
 * Update users list display
 */
function updateUsersList(users) {
    const usersList = document.getElementById('users-list');
    
    // Filter out current user
    const otherUsers = users.filter(u => u.user_id !== currentUserId);
    
    if (otherUsers.length === 0) {
        usersList.innerHTML = '<p class="no-users">No other users connected</p>';
        return;
    }
    
    usersList.innerHTML = otherUsers.map(user => `
        <div class="user-item" style="border-left-color: ${user.color}">
            <div class="user-color" style="background-color: ${user.color}"></div>
            <div class="user-name">${user.user_id}</div>
        </div>
    `).join('');
}

/**
 * Broadcast cursor position
 */
function broadcastCursorPosition() {
    if (!ws || !isConnected) {
        return;
    }
    
    const codeEditor = document.getElementById('code-editor');
    const position = codeEditor.selectionStart;
    
    // Calculate line number
    const text = codeEditor.value.substring(0, position);
    const line = text.split('\n').length;
    
    ws.send(JSON.stringify({
        action: 'cursor_position',
        user_id: currentUserId,
        position: position,
        line: line
    }));
}

/**
 * Setup event listeners
 */
function setupEventListeners() {
    const codeEditor = document.getElementById('code-editor');

    // Handle code changes
    codeEditor.addEventListener('input', () => {
        updateLineNumbers();
        updateEditorInfo();
        broadcastCodeUpdate();
        broadcastCursorPosition();
    });

    // Handle cursor movement
    codeEditor.addEventListener('click', () => {
        broadcastCursorPosition();
    });

    codeEditor.addEventListener('keyup', () => {
        broadcastCursorPosition();
    });

    // Handle tab insertion
    codeEditor.addEventListener('keydown', (event) => {
        if (event.key === 'Tab') {
            event.preventDefault();
            const start = codeEditor.selectionStart;
            const end = codeEditor.selectionEnd;
            codeEditor.value = codeEditor.value.substring(0, start) + '\t' + codeEditor.value.substring(end);
            codeEditor.selectionStart = codeEditor.selectionEnd = start + 1;
            updateLineNumbers();
            broadcastCodeUpdate();
            broadcastCursorPosition();
        }
    });

    // Handle tab switching
    document.getElementById('tab-code').addEventListener('click', () => {
        switchTab('code');
    });

    document.getElementById('tab-autocomplete').addEventListener('click', () => {
        switchTab('autocomplete');
    });

    // Handle sync scroll with line numbers
    codeEditor.addEventListener('scroll', () => {
        const lineNumbers = document.getElementById('line-numbers');
        lineNumbers.scrollTop = codeEditor.scrollTop;
    });
}

/**
 * Broadcast code update to other users
 */
function broadcastCodeUpdate() {
    if (!ws || !isConnected) {
        return;
    }

    const code = document.getElementById('code-editor').value;
    
    ws.send(JSON.stringify({
        action: 'update',
        room_id: roomId,
        code: code,
        user_id: getCurrentUserId()
    }));

    updateSyncStatus('Syncing...');
}

/**
 * Update line numbers
 */
function updateLineNumbers() {
    const codeEditor = document.getElementById('code-editor');
    const lineNumbers = document.getElementById('line-numbers');
    
    const lines = codeEditor.value.split('\n').length;
    let lineNumbersText = '';

    for (let i = 1; i <= lines; i++) {
        lineNumbersText += i + '\n';
    }

    lineNumbers.textContent = lineNumbersText;
}

/**
 * Update editor information
 */
function updateEditorInfo() {
    const code = document.getElementById('code-editor').value;
    const lines = code.split('\n').length;
    const characters = code.length;

    document.getElementById('editor-info').textContent = 
        `Characters: ${characters} | Lines: ${lines}`;
}

/**
 * Update user count
 */
function updateUserCount(count) {
    document.getElementById('user-count').textContent = `${count} user${count !== 1 ? 's' : ''}`;
    document.getElementById('connected-count').textContent = count;
}

/**
 * Update connection status
 */
function updateConnectionStatus(connected) {
    const statusElement = document.getElementById('connection-status');
    const syncElement = document.getElementById('last-sync');

    if (connected) {
        statusElement.textContent = 'Connected';
        statusElement.classList.remove('status-disconnected');
        statusElement.classList.add('status-connected');
        syncElement.classList.add('connected');
        syncElement.textContent = '● Connected';
    } else {
        statusElement.textContent = 'Disconnected';
        statusElement.classList.add('status-disconnected');
        statusElement.classList.remove('status-connected');
        syncElement.classList.remove('connected');
        syncElement.textContent = '● Disconnected';
    }
}

/**
 * Update sync status
 */
function updateSyncStatus(message) {
    document.getElementById('last-sync').textContent = '● ' + message;
}

/**
 * Switch between tabs
 */
function switchTab(tab) {
    // Update tab display
    document.querySelectorAll('.tab').forEach(t => {
        t.classList.remove('active');
    });

    if (tab === 'code') {
        document.getElementById('tab-code').classList.add('active');
        document.getElementById('autocomplete-panel').classList.add('hidden');
    } else if (tab === 'autocomplete') {
        document.getElementById('tab-autocomplete').classList.add('active');
        document.getElementById('autocomplete-panel').classList.remove('hidden');
        fetchAutocomplete();
    }
}

/**
 * Toggle suggestions panel
 */
function toggleSuggestions() {
    const panel = document.getElementById('autocomplete-panel');
    panel.classList.toggle('hidden');
    if (!panel.classList.contains('hidden')) {
        fetchAutocomplete();
    }
}

/**
 * Fetch autocomplete suggestions
 */
async function fetchAutocomplete() {
    try {
        const codeEditor = document.getElementById('code-editor');
        const lastLine = codeEditor.value.split('\n').pop();
        const prefix = lastLine.trim();

        if (prefix.length === 0) {
            document.getElementById('suggestions-list').innerHTML = 
                '<div class="suggestion-item">Start typing to see suggestions</div>';
            return;
        }

        const response = await fetch(`${API_BASE_URL}/autocomplete`, {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
            },
            body: JSON.stringify({
                prefix: prefix,
                language: currentLanguage
            })
        });

        if (!response.ok) {
            throw new Error(`Failed to get suggestions: ${response.statusText}`);
        }

        const data = await response.json();
        displaySuggestions(data.suggestions);
    } catch (error) {
        console.error('Error fetching suggestions:', error);
        document.getElementById('suggestions-list').innerHTML = 
            '<div class="suggestion-item">Error loading suggestions</div>';
    }
}

/**
 * Display suggestions
 */
function displaySuggestions(suggestions) {
    const list = document.getElementById('suggestions-list');
    
    if (!suggestions || suggestions.length === 0) {
        list.innerHTML = '<div class="suggestion-item">No suggestions found</div>';
        return;
    }

    list.innerHTML = suggestions.map(suggestion => `
        <div class="suggestion-item" onclick="insertSuggestion('${suggestion.replace(/'/g, "\\'")}')">
            ${suggestion}
        </div>
    `).join('');
}

/**
 * Insert suggestion into editor
 */
function insertSuggestion(suggestion) {
    const codeEditor = document.getElementById('code-editor');
    const lastNewlineIndex = codeEditor.value.lastIndexOf('\n');
    const beforeLastLine = codeEditor.value.substring(0, lastNewlineIndex + 1);
    
    codeEditor.value = beforeLastLine + suggestion;
    codeEditor.focus();
    updateLineNumbers();
    broadcastCodeUpdate();
}

/**
 * Change language
 */
function changeLanguage(language) {
    currentLanguage = language;
    fetchAutocomplete();
}

/**
 * Clear editor
 */
function clearEditor() {
    if (confirm('Are you sure you want to clear all code?')) {
        document.getElementById('code-editor').value = '';
        updateLineNumbers();
        broadcastCodeUpdate();
    }
}

/**
 * Copy room URL
 */
function copyRoomUrl() {
    const url = `${window.location.origin}${window.location.pathname}?room=${roomId}`;
    navigator.clipboard.writeText(url).then(() => {
        showMessage('Room URL copied to clipboard!');
    }).catch(() => {
        showMessage('Failed to copy URL');
    });
}

/**
 * Get current user ID (generate and store in session)
 */
function getCurrentUserId() {
    let userId = sessionStorage.getItem('userId');
    if (!userId) {
        userId = 'user_' + Math.random().toString(36).substr(2, 9);
        sessionStorage.setItem('userId', userId);
    }
    return userId;
}

/**
 * Show error message
 */
function showErrorMessage(message) {
    showMessage(message, 'error');
}

/**
 * Show message
 */
function showMessage(message, type = 'info') {
    console.log(`[${type.toUpperCase()}] ${message}`);
    // In a production app, you'd show a toast notification here
    alert(message);
}
