// static/js/auth.js

import { initialUserData, getUserSession } from './data.js';

document.addEventListener('DOMContentLoaded', () => {



    const loginForm = document.getElementById('loginForm');
    if (loginForm) {
        // NOTE: This simulation won't actually log you into Django.
        // You need to replace index.html's form with a Django form
        // that POSTs to {% url 'login' %} for real authentication.
        loginForm.addEventListener('submit', (e) => {
            e.preventDefault();
            const email = document.getElementById('email').value;
            const password = document.getElementById('password').value; 

            // Simulate successful login check (replace this with Django form POST)
            if (email === initialUserData.email.toLowerCase() && password === 'test1234') { 
                // Setting localStorage doesn't log you into Django
                localStorage.setItem('autoaudit_session', JSON.stringify(initialUserData)); 

                // Manually redirect after fake login (for now)
                window.location.href = '/dashboard/'; 
            } else {
                alert("Simulated login failed. Use email: meera@autoaudit.in, password: test1234. Or use the superuser account.");
            }
        });
    }

    const registerForm = document.getElementById('registerForm');
    if (registerForm) {
        registerForm.addEventListener('submit', (e) => {
            e.preventDefault();
            // In a real app, you would send this data to a backend.
            alert("Registration simulated successfully! Redirecting to login.");
            window.location.href = '/'; // MODIFIED: Redirect to index (login) URL
        });
    }
});