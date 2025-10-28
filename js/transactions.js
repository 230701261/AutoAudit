// js/transactions.js

import { transactionsData, updateHeader } from './data.js';

document.addEventListener('DOMContentLoaded', () => {
    // 1. Update the common header info
    updateHeader();

    // 2. Render Transactions List
    const transactionList = document.querySelector('.transaction-list');
    if (transactionList) {
        transactionList.innerHTML = transactionsData.map(txn => `
            <div class="transaction-card">
                <div class="card-left">
                    <div class="status-icon ${txn.iconClass}">${txn.icon}</div>
                    <div class="transaction-details">
                        <a href="${txn.link}" style="text-decoration: none; color: inherit;">
                            <h3>${txn.entity} #${txn.id}</h3>
                        </a>
                        <p>${txn.details}</p>
                        <div class="status-row">
                            <span>Amount: ${txn.amount}</span>
                            <span>Status: ${txn.status}</span>
                            <span class="risk-${txn.risk.toLowerCase()}">Risk: ${txn.risk}</span>
                        </div>
                    </div>
                </div>
                <div class="actions">
                    <button class="action-btn view-btn">View Ledger Trail</button>
                    <button class="action-btn assign-btn" onclick="window.location.href='Assign Reviewer Page.html'">Assign Reviewer</button>
                </div>
            </div>
        `).join('');
    }
});