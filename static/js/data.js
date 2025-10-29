// static/js/data.js

// --- 1. SESSION & USER DATA ---
// Keep initialUserData for other JS parts if needed, but header won't use it directly
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
 * Less critical now, mainly for non-auth JS features.
 */
export function getUserSession() {
    const session = localStorage.getItem('autoaudit_session');
    if (session) {
        return JSON.parse(session);
    }
    // Return null or a default empty object if no session found
    // Avoid setting it here if it doesn't exist.
    return null;
}

/**
 * Updates the common header - SIMPLIFIED
 * Now only attaches the logout listener. User info display is handled by Django templates.
 */
export function updateHeader() {
    // Find the logout button which should exist in the Django template now
    const logoutBtn = document.getElementById('logoutBtn');

    // Attach the event listener for the logout button if it exists
    if (logoutBtn) {
        logoutBtn.addEventListener('click', () => {
            localStorage.removeItem('autoaudit_session'); // Clear any simulated session info
            // Redirect to Django logout URL
            window.location.href = '/accounts/logout/';
        });
    }
    // Removed all logic that modifies headerRight.innerHTML
    // Removed all client-side auth checks and redirects
} // End of updateHeader function

// --- 3. PAGE SPECIFIC DATA ---
// (Keep the rest of the file as it was for features like dashboard metrics, anomalies, transactions)

// Dashboard Data
export const dashboardMetrics = {
    totalTransactions: "1.24M",
    anomalyCount: 247,
    complianceScore: "96.4%",
    pendingReviews: 18
};

export const recentAnomalies = [
    { id: "AN001", severity: "CRITICAL", status: "NEW", desc: "Invoice INV-2024-001 appears to be duplicated with different amounts", amount: "₹15,200", link: "/anomalies/" }, // Use Django URL name if available
    { id: "AN002", severity: "HIGH", status: "INVESTIGATING", desc: "GST Mismatch: Input Tax Credit variance detected", amount: "GST ₹10,000", link: "/anomalies/" },
    { id: "AN003", severity: "MEDIUM", status: "NEW", desc: "Unusually high transaction amount detected", amount: "₹2,50,000", link: "/anomalies/" },
    { id: "AN004", severity: "LOW", status: "RESOLVED", desc: "PAN Validation: Invalid PAN format in vendor record", amount: "N/A", link: "/anomalies/" }
];

// Transactions Data
export const transactionsData = [
    { id: "TRX-98432", entity: "Maharashtra Manufacturing Pvt. Ltd.", details: "GST credit reversal mismatch detected for Q2 filings.", amount: "₹12,48,900", status: "Flagged", risk: "High", icon: "⚠️", iconClass: "warning", link: "/transaction-detail/" }, // Use Django URL name if available
    { id: "TRX-98412", entity: "BlueSky Logistics", details: "Vendor invoice series missing supporting documentation.", amount: "₹4,12,670", status: "Under Review", risk: "Medium", icon: "ℹ️", iconClass: "info", link: "/transaction-detail/" },
    { id: "TRX-98221", entity: "MetroMart Retail", details: "TDS deduction validated against Form 26AS records.", amount: "₹86,450", status: "Cleared", risk: "Low", icon: "✅", iconClass: "success", link: "/transaction-detail/" }
];