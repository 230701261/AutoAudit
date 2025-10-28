// js/data.js

// --- 1. SESSION & USER DATA ---
export const initialUserData = {
    username: "Meera Iyer",
    firstName: "Meera",
    role: "Reviewer",
    email: "meera@autoaudit.in",
    notifications: 3
};

// --- 2. GLOBAL UTILITIES ---
/**
 * Retrieves the current user session from local storage.
 */
export function getUserSession() {
    const session = localStorage.getItem('autoaudit_session');
    if (session) {
        return JSON.parse(session);
    }
    return null;
}

/**
 * Updates the common header across all main pages.
 */
export function updateHeader() {
    const user = getUserSession();
    const notificationCount = user ? initialUserData.notifications : 0;
    const headerRight = document.getElementById('header-right-container');

    if (headerRight) {
        // Build the notification bell with content only if count > 0
        const bellContent = notificationCount > 0 ? `<div class="notification-bell">🔔</div>` : ``;

        if (user) {
            headerRight.innerHTML = `
                ${bellContent}
                <div class="user-info" id="header-user-info">
                    <span>${user.firstName}</span>
                    <span class="reviewer-info">Reviewer: ${user.username}</span>
                    <button class="logout-btn" id="logoutBtn">Logout</button>
                </div>
            `;
            // Re-attach event listener for the new logout button
            document.getElementById('logoutBtn')?.addEventListener('click', () => {
                localStorage.removeItem('autoaudit_session');
                // Redirect to the root (index.html, the login page)
                window.location.href = window.location.origin; 
            });
        } else {
            // Redirect to login if no session is found on a protected page
            if (window.location.pathname.includes('/pages/')) {
                window.location.href = window.location.origin;
            }
        }
    }
}

// --- 3. PAGE SPECIFIC DATA ---

// Dashboard Data
export const dashboardMetrics = {
    totalTransactions: "1.24M",
    anomalyCount: 247,
    complianceScore: "96.4%",
    pendingReviews: 18
};

export const recentAnomalies = [
    { id: "AN001", severity: "CRITICAL", status: "NEW", desc: "Invoice INV-2024-001 appears to be duplicated with different amounts", amount: "₹15,200", link: "anomalies.html" },
    { id: "AN002", severity: "HIGH", status: "INVESTIGATING", desc: "GST Mismatch: Input Tax Credit variance detected", amount: "GST ₹10,000", link: "anomalies.html" },
    { id: "AN003", severity: "MEDIUM", status: "NEW", desc: "Unusually high transaction amount detected", amount: "₹2,50,000", link: "anomalies.html" },
    { id: "AN004", severity: "LOW", status: "RESOLVED", desc: "PAN Validation: Invalid PAN format in vendor record", amount: "N/A", link: "anomalies.html" }
];

// Transactions Data
export const transactionsData = [
    { id: "TRX-98432", entity: "Maharashtra Manufacturing Pvt. Ltd.", details: "GST credit reversal mismatch detected for Q2 filings.", amount: "₹12,48,900", status: "Flagged", risk: "High", icon: "⚠️", iconClass: "warning", link: "Transaction Detail Page.html" },
    { id: "TRX-98412", entity: "BlueSky Logistics", details: "Vendor invoice series missing supporting documentation.", amount: "₹4,12,670", status: "Under Review", risk: "Medium", icon: "ℹ️", iconClass: "info", link: "Transaction Detail Page.html" },
    { id: "TRX-98221", entity: "MetroMart Retail", details: "TDS deduction validated against Form 26AS records.", amount: "₹86,450", status: "Cleared", risk: "Low", icon: "✅", iconClass: "success", link: "Transaction Detail Page.html" }
];