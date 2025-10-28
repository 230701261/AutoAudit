// js/dashboard.js

import { dashboardMetrics, recentAnomalies, updateHeader } from './data.js';

document.addEventListener('DOMContentLoaded', () => {
    // 1. Update the common header info
    updateHeader();

    // 2. Render Metrics Grid
    const metricCards = document.querySelectorAll('.metrics-grid .metric-card');
    if (metricCards.length >= 4) {
        // Total Transactions
        metricCards[0].querySelector('.value').textContent = dashboardMetrics.totalTransactions;
        // Detected Anomalies
        metricCards[1].querySelector('.value').textContent = dashboardMetrics.anomalyCount;
        // Compliance Score
        metricCards[2].querySelector('.value').textContent = dashboardMetrics.complianceScore;
        // Pending Reviews
        metricCards[3].querySelector('.value').textContent = dashboardMetrics.pendingReviews;
    }

    // 3. Render Recent Anomalies
    const anomaliesContainer = document.getElementById('recent-anomalies-list');
    if (anomaliesContainer) {
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
    }

    // --- NEWLY ADDED: Chatbot Logic ---
    const chatToggle = document.getElementById('chatbot-toggle');
    const chatContainer = document.getElementById('chatbot-container');
    const chatClose = document.getElementById('chatbot-close');
    const chatMessages = document.getElementById('chat-messages');
    const chatInput = document.getElementById('chat-input');
    const chatSendBtn = document.getElementById('chat-send-btn');

    // Toggle chat window
    if (chatToggle && chatContainer) {
        chatToggle.addEventListener('click', () => {
            chatContainer.classList.toggle('hidden');
            chatToggle.classList.toggle('hidden'); // Also hide the FAB
        });
    }

    // Close chat window
    if (chatClose && chatContainer && chatToggle) {
        chatClose.addEventListener('click', () => {
            chatContainer.classList.add('hidden');
            chatToggle.classList.remove('hidden'); // Show the FAB
        });
    }

    // Function to add a message to the chat
    const addChatMessage = (sender, message) => {
        const msgDiv = document.createElement('div');
        msgDiv.classList.add('chat-message');
        msgDiv.classList.add(sender === 'user' ? 'user' : 'bot');
        msgDiv.textContent = message;
        chatMessages.appendChild(msgDiv);
        // Scroll to the bottom
        chatMessages.scrollTop = chatMessages.scrollHeight;
    };

    // Function to get a dummy bot response
    const getBotResponse = (userInput) => {
        const normalizedInput = userInput.toLowerCase();
        let response;

        if (normalizedInput.includes('hello') || normalizedInput.includes('hi')) {
            response = "Hi there! What can I help you find?";
        } else if (normalizedInput.includes('anomalies')) {
            response = "I found 247 anomalies. The most critical is 'AN001' related to duplicate invoices. Would you like to navigate there?";
        } else if (normalizedInput.includes('compliance')) {
            response = "The overall compliance score is 96.4%. TDS Compliance is the lowest at 78%.";
        } else if (normalizedInput.includes('report')) {
            response = "You can generate reports from the 'Reports' tab. What kind of report do you need?";
        } else {
            response = `I am a dummy bot. I received your message: "${userInput}"`;
        }

        // Simulate bot "thinking" time
        setTimeout(() => {
            addChatMessage('bot', response);
        }, 1200);
    };

    // Function to handle sending a message
    const sendMessage = () => {
        const message = chatInput.value.trim();
        if (message === '') return;

        addChatMessage('user', message);
        chatInput.value = ''; // Clear input

        getBotResponse(message);
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
    }
    // --- END NEWLY ADDED ---
});