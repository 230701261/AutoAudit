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
});