// static/js/dashboard.js

import { dashboardMetrics, recentAnomalies, updateHeader } from './data.js';

// --- NEW: Function to get CSRF token ---
function getCookie(name) {
    let cookieValue = null;
    if (document.cookie && document.cookie !== '') {
        const cookies = document.cookie.split(';');
        for (let i = 0; i < cookies.length; i++) {
            const cookie = cookies[i].trim();
            // Does this cookie string begin with the name we want?
            if (cookie.substring(0, name.length + 1) === (name + '=')) {
                cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
                break;
            }
        }
    }
    return cookieValue;
}
const csrftoken = getCookie('csrftoken'); // Get the token once
// --- End CSRF function ---


document.addEventListener('DOMContentLoaded', () => {
    // 1. Update header (Ensure updateHeader exists in data.js and works)
    if(typeof updateHeader === 'function') {
        updateHeader();
    } else {
        console.error("updateHeader function not found in data.js");
    }


    // 2. Render Metrics Grid (Ensure dashboardMetrics exists)
    const metricCards = document.querySelectorAll('.metrics-grid .metric-card');
    if (metricCards.length >= 4 && typeof dashboardMetrics !== 'undefined') {
        metricCards[0].querySelector('.value').textContent = dashboardMetrics.totalTransactions;
        metricCards[1].querySelector('.value').textContent = dashboardMetrics.anomalyCount;
        metricCards[2].querySelector('.value').textContent = dashboardMetrics.complianceScore;
        metricCards[3].querySelector('.value').textContent = dashboardMetrics.pendingReviews;
    } else {
        console.warn("Could not render dashboard metrics: Elements or data missing.");
    }


    // 3. Render Recent Anomalies (Ensure recentAnomalies exists)
    const anomaliesContainer = document.getElementById('recent-anomalies-list');
    if (anomaliesContainer && typeof recentAnomalies !== 'undefined') {
        anomaliesContainer.innerHTML = recentAnomalies.map(anomaly => `
            <a href="${anomaly.link}" class="anomaly-item">
                <div class="anomaly-main">
                    <div class="anomaly-type">
                        <span class="severity-badge severity-${anomaly.severity.toLowerCase()}">${anomaly.id} ${anomaly.severity}</span>
                        <span class="status-badge">${anomaly.status}</span>
                    </div>
                    <div class="anomaly-desc">${anomaly.desc}</div>
                    <div class="anomaly-meta">${anomaly.amount} | Oct 15, 2025 12:15 PM</div>
                </div>
                <div class="anomaly-actions">
                    <div class="action-icon">⋮</div>
                </div>
            </a>
        `).join('');
    } else {
         console.warn("Could not render recent anomalies: Element or data missing.");
    }


    // --- MODIFIED: Chatbot Logic ---
    const chatToggle = document.getElementById('chatbot-toggle');
    const chatContainer = document.getElementById('chatbot-container');
    const chatClose = document.getElementById('chatbot-close');
    const chatMessages = document.getElementById('chat-messages');
    const chatInput = document.getElementById('chat-input');
    const chatSendBtn = document.getElementById('chat-send-btn');

    // --- NEW: Django API endpoint URL ---
    const CHATBOT_API_URL = '/api/chatbot/'; // Your Django endpoint

    // Toggle chat window
    if (chatToggle && chatContainer) {
        chatToggle.addEventListener('click', () => {
            chatContainer.classList.toggle('hidden');
            chatToggle.classList.toggle('hidden');
        });
    }

    // Close chat window
    if (chatClose && chatContainer && chatToggle) {
        chatClose.addEventListener('click', () => {
            chatContainer.classList.add('hidden');
            chatToggle.classList.remove('hidden');
        });
    }

    // Function to add a message to the chat
    const addChatMessage = (sender, message) => {
        if (!chatMessages) {
             console.error("Chat messages container not found!");
             return;
        }
        const msgDiv = document.createElement('div');
        msgDiv.classList.add('chat-message');
        msgDiv.classList.add(sender === 'user' ? 'user' : 'bot');
        // Sanitize message slightly (basic protection)
        msgDiv.textContent = message;
        chatMessages.appendChild(msgDiv);
        chatMessages.scrollTop = chatMessages.scrollHeight; // Scroll to bottom
    };

    // --- MODIFIED: getBotResponse to call Django API ---
    const getBotResponse = async (userInput) => {
        addChatMessage('bot', 'Thinking...');

        try {
            const response = await fetch(CHATBOT_API_URL, { // Call your backend
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                    // 'X-CSRFToken': csrftoken // Uncomment if you remove @csrf_exempt
                },
                body: JSON.stringify({
                    message: userInput // Send message in expected format
                })
            });

            // Remove thinking message
            const thinkingMessage = chatMessages?.lastElementChild;
            if (thinkingMessage && thinkingMessage.textContent === 'Thinking...' && thinkingMessage.classList.contains('bot')) {
                 chatMessages.removeChild(thinkingMessage);
            }

            const data = await response.json(); // Expect JSON from Django

            if (!response.ok) {
                 // Use error message from Django response if available
                console.error("Backend API Error:", data); // Log the error object from Django
                throw new Error(data.error || `Request failed with status ${response.status}`);
            }

            // Expecting {"response": "AI text"} from Django
            const botText = data.response || "Sorry, I received an empty response.";
            addChatMessage('bot', botText);

        } catch (error) {
            console.error("Error fetching bot response from backend:", error);
             // Ensure thinking message is removed even on fetch failure
            const thinkingMessage = chatMessages?.lastElementChild;
            if (thinkingMessage && thinkingMessage.textContent === 'Thinking...' && thinkingMessage.classList.contains('bot')) {
                 chatMessages.removeChild(thinkingMessage);
            }
            // Display a user-friendly error message
            addChatMessage('bot', `Sorry, could not connect to the AI assistant. ${error.message}`);
        }
    };

    // Function to handle sending a message
    const sendMessage = () => {
         if (!chatInput) {
             console.error("Chat input element not found!");
             return; // Add check
         }
         const message = chatInput.value.trim();
         if (message === '') return;
         addChatMessage('user', message);
         chatInput.value = '';
         getBotResponse(message); // Call async function
     };

    // Event listeners for sending
    if (chatSendBtn) {
        chatSendBtn.addEventListener('click', sendMessage);
    }
    if (chatInput) {
        chatInput.addEventListener('keypress', (e) => {
            if (e.key === 'Enter') {
                sendMessage();
            }
        });
    } else {
        console.warn("Chat input element not found during listener setup.");
    }
    // --- END MODIFIED Chatbot Logic ---
});