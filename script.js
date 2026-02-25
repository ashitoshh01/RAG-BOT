const chatMessages = document.getElementById('chat-messages');
const userInput = document.getElementById('user-input');
const sendButton = document.getElementById('send-button');

// We are calling the FastAPI endpoint on the same server, so relative URL works
const API_URL = '/chat';

function addMessage(text, sender) {
    const messageDiv = document.createElement('div');
    messageDiv.classList.add('message', sender === 'user' ? 'user-message' : 'bot-message');
    
    const contentDiv = document.createElement('div');
    contentDiv.classList.add('message-content');
    contentDiv.textContent = text;
    
    messageDiv.appendChild(contentDiv);
    chatMessages.appendChild(messageDiv);
    
    // Auto scroll
    chatMessages.scrollTop = chatMessages.scrollHeight;
}

function addLoadingIndicator() {
    const messageDiv = document.createElement('div');
    messageDiv.classList.add('message', 'bot-message');
    messageDiv.id = 'loading-indicator';
    
    const contentDiv = document.createElement('div');
    contentDiv.classList.add('message-content', 'loading');
    
    for (let i = 0; i < 3; i++) {
        const dot = document.createElement('span');
        contentDiv.appendChild(dot);
    }
    
    messageDiv.appendChild(contentDiv);
    chatMessages.appendChild(messageDiv);
    chatMessages.scrollTop = chatMessages.scrollHeight;
}

function removeLoadingIndicator() {
    const loadingIds = document.querySelectorAll('#loading-indicator');
    loadingIds.forEach(el => el.remove());
}

async function sendMessage() {
    const text = userInput.value.trim();
    if (!text) return;
    
    // Add user message
    addMessage(text, 'user');
    userInput.value = '';
    
    // Add loading
    addLoadingIndicator();
    
    try {
        const response = await fetch(API_URL, {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json'
            },
            body: JSON.stringify({ message: text })
        });
        
        removeLoadingIndicator();
        
        if (!response.ok) {
            throw new Error(`HTTP error! status: ${response.status}`);
        }
        
        const data = await response.json();
        addMessage(data.answer, 'bot');
    } catch (error) {
        removeLoadingIndicator();
        addMessage("Sorry, I encountered an error connecting to the server.", 'bot');
        console.error("Error:", error);
    }
}

sendButton.addEventListener('click', sendMessage);
userInput.addEventListener('keypress', (e) => {
    if (e.key === 'Enter') {
        sendMessage();
    }
});
