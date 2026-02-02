// ============================================
// MODERN HEALTH CHATBOT - JAVASCRIPT
// Enhanced chat functionality with better UX
// ============================================

// DOM Elements
const chatBox = document.getElementById('chatBox');
const chatForm = document.getElementById('chatForm');
const userInput = document.getElementById('user-input');
const sendBtn = document.getElementById('send-btn');

// Configuration
const CONFIG = {
    API_ENDPOINT: '/api/chat',
    HISTORY_ENDPOINT: '/api/history',
    MAX_RETRIES: 3,
    RETRY_DELAY: 1000,
    TYPING_DELAY: 500
};

// State
let isProcessing = false;
let messageQueue = [];

// ============================================
// INITIALIZATION
// ============================================

document.addEventListener('DOMContentLoaded', () => {
    initializeChat();
    loadChatHistory();
    setupEventListeners();
});

function initializeChat() {
    console.log('🤖 Health Chatbot initialized');
    userInput.focus();
}

// ============================================
// EVENT LISTENERS
// ============================================

function setupEventListeners() {
    // Form submission
    chatForm.addEventListener('submit', handleSubmit);
    
    // Enter key to send (Shift+Enter for new line)
    userInput.addEventListener('keydown', (e) => {
        if (e.key === 'Enter' && !e.shiftKey) {
            e.preventDefault();
            chatForm.dispatchEvent(new Event('submit'));
        }
    });
    
    // Auto-resize textarea (if converting to textarea)
    userInput.addEventListener('input', () => {
        // Auto-grow input if needed
        adjustInputHeight();
    });
}

function adjustInputHeight() {
    if (userInput.scrollHeight > userInput.clientHeight) {
        userInput.style.height = 'auto';
        userInput.style.height = Math.min(userInput.scrollHeight, 120) + 'px';
    }
}

// ============================================
// MESSAGE HANDLING
// ============================================

async function handleSubmit(e) {
    e.preventDefault();
    
    const message = userInput.value.trim();
    if (!message || isProcessing) return;
    
    // Add user message
    addMessage(message, 'user');
    userInput.value = '';
    userInput.style.height = 'auto';
    
    // Set processing state
    setProcessingState(true);
    showTypingIndicator();
    
    try {
        // Send message to server
        const response = await sendMessage(message);
        
        // Hide typing indicator
        hideTypingIndicator();
        
        // Add bot response
        if (response && response.reply) {
            addMessage(response.reply, 'bot');
        } else {
            throw new Error('Invalid response format');
        }
    } catch (error) {
        console.error('Chat error:', error);
        hideTypingIndicator();
        addMessage('⚠️ Sorry, I encountered an error. Please try again.', 'bot');
    } finally {
        setProcessingState(false);
    }
}

async function sendMessage(message, retries = 0) {
    try {
        const response = await fetch(CONFIG.API_ENDPOINT, {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
            },
            body: JSON.stringify({ message })
        });
        
        if (!response.ok) {
            throw new Error(`HTTP error! status: ${response.status}`);
        }
        
        return await response.json();
        
    } catch (error) {
        // Retry logic
        if (retries < CONFIG.MAX_RETRIES) {
            console.log(`Retry attempt ${retries + 1}/${CONFIG.MAX_RETRIES}`);
            await sleep(CONFIG.RETRY_DELAY);
            return sendMessage(message, retries + 1);
        }
        throw error;
    }
}

// ============================================
// MESSAGE DISPLAY
// ============================================

function addMessage(text, sender) {
    const messageDiv = document.createElement('div');
    messageDiv.className = `message ${sender}`;
    
    // Create avatar
    const avatar = document.createElement('div');
    avatar.className = 'message-avatar';
    avatar.textContent = sender === 'user' ? '👤' : '🤖';
    
    // Create message content
    const content = document.createElement('div');
    content.className = 'message-content';
    
    // Format message (support for markdown-like formatting)
    content.innerHTML = formatMessage(text);
    
    // Append elements
    messageDiv.appendChild(avatar);
    messageDiv.appendChild(content);
    
    // Add to chat
    chatBox.appendChild(messageDiv);
    
    // Smooth scroll to bottom
    scrollToBottom();
    
    // Animate message entrance
    requestAnimationFrame(() => {
        messageDiv.style.opacity = '0';
        messageDiv.style.transform = 'translateY(10px)';
        requestAnimationFrame(() => {
            messageDiv.style.transition = 'all 0.3s ease-out';
            messageDiv.style.opacity = '1';
            messageDiv.style.transform = 'translateY(0)';
        });
    });
}

function formatMessage(text) {
    // Convert newlines to <br>
    let formatted = text.replace(/\n/g, '<br>');
    
    // Bold text **text**
    formatted = formatted.replace(/\*\*(.*?)\*\*/g, '<strong>$1</strong>');
    
    // Italic text *text*
    formatted = formatted.replace(/\*(.*?)\*/g, '<em>$1</em>');
    
    // Code blocks `code`
    formatted = formatted.replace(/`(.*?)`/g, '<code>$1</code>');
    
    // Bullet points
    formatted = formatted.replace(/^• /gm, '&bull; ');
    
    return formatted;
}

// ============================================
// TYPING INDICATOR
// ============================================

function showTypingIndicator() {
    const indicator = document.createElement('div');
    indicator.id = 'typing-indicator';
    indicator.className = 'message bot';
    indicator.innerHTML = `
        <div class="message-avatar">🤖</div>
        <div class="message-content">
            <div class="typing-indicator active">
                <div class="typing-dot"></div>
                <div class="typing-dot"></div>
                <div class="typing-dot"></div>
            </div>
        </div>
    `;
    chatBox.appendChild(indicator);
    scrollToBottom();
}

function hideTypingIndicator() {
    const indicator = document.getElementById('typing-indicator');
    if (indicator) {
        indicator.remove();
    }
}

// ============================================
// CHAT HISTORY
// ============================================

async function loadChatHistory() {
    try {
        const response = await fetch(CONFIG.HISTORY_ENDPOINT);
        const data = await response.json();
        
        if (data.history && data.history.length > 0) {
            // Clear welcome message if history exists
            const welcome = document.querySelector('.welcome-message');
            if (welcome && data.history.length > 5) {
                welcome.style.display = 'none';
            }
            
            // Add messages
            data.history.forEach(msg => {
                const sender = msg.is_user_message ? 'user' : 'bot';
                addMessageInstant(msg.message, sender);
            });
            
            scrollToBottom();
        }
    } catch (error) {
        console.log('No chat history to load');
    }
}

function addMessageInstant(text, sender) {
    // Add message without animation (for history loading)
    const messageDiv = document.createElement('div');
    messageDiv.className = `message ${sender}`;
    
    const avatar = document.createElement('div');
    avatar.className = 'message-avatar';
    avatar.textContent = sender === 'user' ? '👤' : '🤖';
    
    const content = document.createElement('div');
    content.className = 'message-content';
    content.innerHTML = formatMessage(text);
    
    messageDiv.appendChild(avatar);
    messageDiv.appendChild(content);
    chatBox.appendChild(messageDiv);
}

// ============================================
// UI STATE MANAGEMENT
// ============================================

function setProcessingState(processing) {
    isProcessing = processing;
    sendBtn.disabled = processing;
    userInput.disabled = processing;
    
    if (processing) {
        sendBtn.innerHTML = '<span class="loading"></span>';
    } else {
        sendBtn.textContent = 'Send';
        userInput.focus();
    }
}

function scrollToBottom() {
    chatBox.scrollTo({
        top: chatBox.scrollHeight,
        behavior: 'smooth'
    });
}

// ============================================
// UTILITY FUNCTIONS
// ============================================

function sleep(ms) {
    return new Promise(resolve => setTimeout(resolve, ms));
}

function escapeHtml(text) {
    const map = {
        '&': '&amp;',
        '<': '&lt;',
        '>': '&gt;',
        '"': '&quot;',
        "'": '&#039;'
    };
    return text.replace(/[&<>"']/g, m => map[m]);
}

// ============================================
// KEYBOARD SHORTCUTS
// ============================================

document.addEventListener('keydown', (e) => {
    // Ctrl/Cmd + K to focus input
    if ((e.ctrlKey || e.metaKey) && e.key === 'k') {
        e.preventDefault();
        userInput.focus();
    }
    
    // Escape to clear input
    if (e.key === 'Escape') {
        userInput.value = '';
        userInput.blur();
    }
});

// ============================================
// ERROR HANDLING
// ============================================

window.addEventListener('error', (e) => {
    console.error('Global error:', e.error);
});

window.addEventListener('unhandledrejection', (e) => {
    console.error('Unhandled promise rejection:', e.reason);
});

// ============================================
// EXPORT FOR DEBUGGING
// ============================================

if (typeof window !== 'undefined') {
    window.chatDebug = {
        addMessage,
        loadChatHistory,
        clearChat: () => {
            chatBox.innerHTML = '';
        }
    };
}

console.log('✅ Chat JavaScript loaded successfully');
