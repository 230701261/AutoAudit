// static/js/transactions.js

import { transactionsData, updateHeader } from './data.js';

// --- Data for new transactions (keep as before) ---
const newTransactionsAfterSync = [
    { id: "TRX-BANK-001", entity: "Ram Text Industry", details: "Incoming payment received via NEFT.", amount: "₹5,50,000", status: "Cleared", risk: "Low", icon: "✅", iconClass: "success", link: "/transaction-detail/" },
    { id: "TRX-BANK-002", entity: "Supplier Payments Inc.", details: "Batch payment processed, reconciliation pending.", amount: "₹-11,20,300", status: "Pending", risk: "Medium", icon: "ℹ️", iconClass: "info", link: "/transaction-detail/" },
    { id: "TRX-BANK-003", entity: "Unknown Beneficiary", details: "Unusual outward transfer detected, requires verification.", amount: "₹-95,000", status: "Flagged", risk: "High", icon: "⚠️", iconClass: "warning", link: "/transaction-detail/" }
];

// --- Helper function createTransactionCardHTML (keep as before) ---
function createTransactionCardHTML(txn) {
    const escapeHTML = (str) => String(str).replace(/[&<>"']/g, match => ({ '&': '&amp;', '<': '&lt;', '>': '&gt;', '"': '&quot;', "'": '&#39;' }[match]));
    // ... (rest of the function is the same, returning the HTML string) ...
    return `
        <div class="transaction-card">
            <div class="card-left">
                <div class="status-icon ${escapeHTML(txn.iconClass)}">${escapeHTML(txn.icon)}</div>
                <div class="transaction-details">
                    <a href="${escapeHTML(txn.link)}" style="text-decoration: none; color: inherit;">
                        <h3>${escapeHTML(txn.entity)} #${escapeHTML(txn.id)}</h3>
                    </a>
                    <p>${escapeHTML(txn.details)}</p>
                    <div class="status-row">
                        <span>Amount: ${escapeHTML(txn.amount)}</span>
                        <span>Status: ${escapeHTML(txn.status)}</span>
                        <span class="risk-${escapeHTML(txn.risk.toLowerCase())}">Risk: ${escapeHTML(txn.risk)}</span>
                    </div>
                </div>
            </div>
            <div class="actions">
                <button class="action-btn view-btn">View Ledger Trail</button>
                <button class="action-btn assign-btn" onclick="window.location.href='/assign-reviewer/'">Assign Reviewer</button>
            </div>
        </div>
    `;
}


document.addEventListener('DOMContentLoaded', () => {
    console.log("DOM loaded for transactions.js");

    // 1. Update Header (keep as before)
    if (typeof updateHeader === 'function') updateHeader(); else console.error("updateHeader function not found.");

    // 2. Render Initial Transactions (keep as before)
    const initialTransactionContainer = document.querySelector('.transaction-list');
    if (initialTransactionContainer && typeof transactionsData !== 'undefined') {
        initialTransactionContainer.innerHTML = transactionsData.map(createTransactionCardHTML).join('');
        console.log("Initial transactions rendered.");
    } else { console.warn("Could not render initial transactions."); }

    // --- Bank Sync Feature ---
    const syncBtn = document.getElementById('sync-bank-btn');
    const syncStatus = document.getElementById('sync-status-message');

    if (syncBtn && syncStatus) {
        console.log("Adding click listener to Sync button.");
        syncBtn.addEventListener('click', () => {
            console.log("Sync button clicked!");
            // 1. Show loading
            syncStatus.innerHTML = '<div class="loader"></div> Syncing started...';
            syncBtn.disabled = true;
            syncStatus.style.display = 'flex';
            console.log("Showing sync started message.");

            // 2. Simulate delay
            setTimeout(() => {
                console.log("Simulated sync finished.");
                // 3. Update status message
                syncStatus.innerHTML = '✅ Syncing completed.';
                syncBtn.disabled = false;

                // --- MODIFIED: Add new transactions ---
                const currentTransactionContainer = document.querySelector('.transaction-list');

                if (currentTransactionContainer) {
                    console.log("Transaction list container FOUND:", currentTransactionContainer);
                    console.log(">>> INNER HTML BEFORE APPEND:\n", currentTransactionContainer.innerHTML.substring(0, 500) + "..."); // LOG BEFORE

                    try {
                        newTransactionsAfterSync.forEach((newTxn, index) => {
                            const newCardHTML = createTransactionCardHTML(newTxn);
                            const tempDiv = document.createElement('div');
                            tempDiv.innerHTML = newCardHTML.trim();
                            const newCardElement = tempDiv.firstChild;

                            if (newCardElement) {
                                console.log(`Attempting to append element for item ${index + 1}...`);
                                currentTransactionContainer.appendChild(newCardElement);
                                console.log(`Appended transaction ${index + 1}: ${newTxn.entity}`);
                            } else {
                                console.error(`!!! Failed to create element from HTML for item ${index + 1}`);
                            }
                        });
                        // Add logging AFTER the loop finishes
                        console.log("✅ Append loop finished.");
                        console.log(">>> INNER HTML AFTER APPEND:\n", currentTransactionContainer.innerHTML.substring(0, 500) + "..."); // LOG AFTER

                    } catch (error) {
                        console.error("!!! Error during the process of appending new transaction HTML:", error);
                        syncStatus.innerHTML = 'Error adding new transactions!';
                        syncStatus.style.color = 'red';
                    }
                } else {
                    console.error("!!! Transaction list container (.transaction-list) NOT FOUND when trying to append.");
                    syncStatus.innerHTML = 'Error: Could not find list to add transactions to!';
                    syncStatus.style.color = 'red';
                }
                // --- End Modification ---

                // 4. Hide status message after delay
                setTimeout(() => {
                    if (syncStatus) {
                        syncStatus.style.display = 'none';
                        syncStatus.innerHTML = '';
                        syncStatus.style.color = '';
                    }
                }, 3000);

            }, 3000); // 3 second delay
        });
    } else {
         if (!syncBtn) console.error("Sync button (#sync-bank-btn) NOT FOUND.");
         if (!syncStatus) console.error("Sync status element (#sync-status-message) NOT FOUND.");
    }
});

// Cookie function (keep if needed)
function getCookie(name) { /* ... */ }