#  AutoAudit – Intelligent Financial Compliance & Audit System

AutoAudit is a full-stack web application designed to automate financial auditing, compliance checking, and anomaly detection using Machine Learning and AI-powered insights. It streamlines auditing workflows, improves accuracy, and provides actionable insights for auditors and organizations.

---

##  Project Overview

AutoAudit helps organizations:

- Detect financial anomalies
- Ensure GST & TDS compliance
- Automate audit workflows
- Visualize financial insights
- Interact with AI chatbot for queries

It combines **Django backend**, **ML models**, and **interactive dashboards** to create a smart auditing ecosystem.

---

##  Key Features

###  Authentication System
- User Registration & Login
- Secure session-based authentication
- Role-ready architecture (extendable)

---

###  Dashboard & Audit Modules
- Financial dashboard overview
- Transactions monitoring
- Anomaly detection system
- Compliance tracking

---

###  AI Chatbot
- Integrated with Google Gemini API
- Answers financial & compliance queries
- Real-time AI interaction

---

###  ML-Based Compliance System
- Predicts:
  - GST Compliance
  - TDS Compliance
- Uses trained ML model
- Accepts real-time inputs

---

###  Data Upload & Analysis
- Upload CSV / Excel files
- Automatic processing
- Generates:
  - Compliance predictions
  - Graphical insights

---

###  Visualization
- Bar charts (Compliance Summary)
- Scatter plots (Score vs Anomalies)
- Distribution graphs

---

###  Policy & Checklist Management
- Upload compliance policies
- GST, TDS, Company Law checklists
- Audit trail tracking

---

##  Tech Stack

### 🔹 Backend
- Django (Python)
- Django Authentication System

### 🔹 Frontend
- HTML, CSS
- Django Templates

### 🔹 Machine Learning
- Pandas
- Scikit-learn (via custom model)
- Custom compliance prediction logic

### 🔹 Visualization
- Matplotlib
- Seaborn

### 🔹 AI Integration
- Google Generative AI (Gemini API)

---

##  Project Structure

```

autoaudit_backend/
│
├── audit/
│   ├── views.py
│   ├── models.py
│   ├── forms.py
│   ├── ml_compliance.py
│   └── urls.py
│
├── templates/
│   ├── index.html
│   ├── RegisterPage.html
│   ├── dashboard.html
│   ├── compliance_results.html
│   └── ...
│
├── static/
│   ├── css/
│   └── js/
│
├── db.sqlite3
├── manage.py
└── README.md

````

---

##  Installation & Setup

###  1. Clone Repository

```bash
git clone https://github.com/230701261/AutoAudit.git
cd autoaudit_backend
````

---

###  2. Create Virtual Environment

```bash
python -m venv venv
venv\Scripts\activate   # Windows
```

---

###  3. Install Dependencies

```bash
pip install -r requirements.txt
```

---

###  4. Run Migrations

```bash
python manage.py makemigrations
python manage.py migrate
```

---

###  5. Create Superuser

```bash
python manage.py createsuperuser
```

---

###  6. Run Server

```bash
python manage.py runserver
```

---

###  7. Open in Browser

```
http://127.0.0.1:8000/
```

---

##  Environment Variables (Important)

 Do NOT expose API keys in code.

Instead use:

```
GOOGLE_API_KEY=your_api_key_here
```

---

##  Future Enhancements

* Role-based access (Auditor, Admin, Reviewer)
* Real-time alerts system
* Advanced ML models
* Deployment on cloud (AWS / Render)
* REST API integration
* Mobile app support

---

##  Learning Outcomes

* Full-stack Django development
* Authentication & session management
* ML model integration into web apps
* Data visualization pipelines
* API integration (AI chatbot)

---

##  Contribution

Feel free to fork and improve the project. Pull requests are welcome.

---

##  License

This project is for educational and research purposes.

---

##  Author

**Ramalingam S**
Computer Science & Engineering
Machine Learning Engineer | Full Stack Developer

---

##  Support

If you found this useful:

👉 Star the repo
👉 Share with others
👉 Build on top of it


