// js/auth.js

import { initialUserData, getUserSession } from './data.js';

document.addEventListener('DOMContentLoaded', () => {
    // Redirect to dashboard if already logged in on a non-main page
    if (getUserSession() && (window.location.pathname.endsWith('index.html') || window.location.pathname.endsWith('/'))) {
        window.location.href = 'pages/dashboard.html';
        return;
    }

    const loginForm = document.getElementById('loginForm');
    if (loginForm) {
        loginForm.addEventListener('submit', (e) => {
            e.preventDefault();
            const email = document.getElementById('email').value;
            const password = document.getElementById('password').value; // In a real app, this is hashed!

            // Simulate successful login check
            if (email === initialUserData.email.toLowerCase() && password === 'test1234') { 
                localStorage.setItem('autoaudit_session', JSON.stringify(initialUserData));
                window.location.href = 'pages/dashboard.html';
            } else {
                alert("Login failed. Use email: meera@autoaudit.in, password: test1234");
            }
        });
    }

    const registerForm = document.getElementById('registerForm');
    if (registerForm) {
        registerForm.addEventListener('submit', (e) => {
            e.preventDefault();
            // In a real app, you would send this data to a backend.
            alert("Registration simulated successfully! Redirecting to login.");
            window.location.href = 'index.html';
        });
    }
});