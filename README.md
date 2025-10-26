📘 EV Charging Anomaly Detection System - Complete README

📌 Table of Contents

Project Overview
What Does This Project Do?
Technology Stack
Project Architecture
Features
Prerequisites
Installation Guide
How to Run the Project
How to Use the Application
Project Structure
API Documentation
Machine Learning Models
Database Schema
Troubleshooting
Future Enhancements


🎯 Project Overview
What is This Project?
This is an intelligent monitoring system for Electric Vehicle (EV) charging stations. It automatically detects suspicious activities and fraudulent behavior in real-time by analyzing charging session data using Machine Learning.
Real-World Problem It Solves:

Billing Fraud: People using high amounts of electricity but paying very little
DoS Attacks: Malicious users booking charging slots repeatedly for very short durations, blocking genuine users
Multi-User Conflicts: Multiple users trying to use the same charger at the same time

Think of it as a security guard that never sleeps, constantly monitoring all charging sessions and alerting you when something suspicious happens.

🎨 What Does This Project Do?
Simple Explanation:
Imagine you own 100 EV charging stations. Every day, thousands of people charge their vehicles. Some people might try to:

Charge their car but trick the system to pay less
Book charging slots but never use them (blocking others)
Use someone else's account

This system automatically:

✅ Reads charging session data from a CSV file
✅ Analyzes each session using AI/Machine Learning
✅ Detects anomalies (suspicious activities)
✅ Shows you a beautiful dashboard with all the alerts
✅ Saves everything to a database for future reference
✅ Lets you take action (flag users, acknowledge alerts)


🛠️ Technology Stack
Frontend (What Users See)

React.js - JavaScript library for building the user interface
TypeScript - Adds type safety to JavaScript (fewer bugs!)
Vite - Super fast build tool
Tailwind CSS - Modern styling framework
shadcn/ui - Beautiful pre-built UI components
Recharts - Interactive charts and graphs
Axios - For communicating with the backend

Backend (The Brain)

Python 3.8+ - Programming language
FastAPI - Modern web framework (handles API requests)
Uvicorn - Server that runs FastAPI
Pandas - Data manipulation and analysis
NumPy - Mathematical operations

Machine Learning (The Detective)

Scikit-learn - ML library for anomaly detection
Isolation Forest - Algorithm that finds unusual patterns
Pre-trained Models - .pkl files containing trained models

Database (The Memory)

MongoDB - Stores all anomaly records
PyMongo - Python driver for MongoDB


🏗️ Project Architecture
┌─────────────────────────────────────────────────────────────────┐
│                          USER                                    │
│                  (Uploads CSV, Views Dashboard)                  │
└────────────────────────────┬────────────────────────────────────┘
                             │
                             ▼
┌─────────────────────────────────────────────────────────────────┐
│                    FRONTEND (React)                              │
│  ┌──────────────┐  ┌──────────────┐  ┌──────────────┐          │
│  │  Dashboard   │  │  File Upload │  │  Analytics   │          │
│  └──────────────┘  └──────────────┘  └──────────────┘          │
└────────────────────────────┬────────────────────────────────────┘
                             │ HTTP Requests
                             ▼
┌─────────────────────────────────────────────────────────────────┐
│                    BACKEND (FastAPI)                             │
│  ┌──────────────────────────────────────────────────────────┐   │
│  │  POST /predict/  - Upload CSV & Get Predictions         │   │
│  │  GET  /logs/     - Fetch Historical Data                │   │
│  └──────────────────────────────────────────────────────────┘   │
└────────────┬──────────────────────────┬─────────────────────────┘
             │                          │
             ▼                          ▼
┌─────────────────────────┐  ┌──────────────────────────┐
│   MACHINE LEARNING      │  │      MONGODB             │
│  ┌──────────────────┐   │  │  ┌──────────────────┐    │
│  │ Isolation Forest │   │  │  │ Anomalies        │    │
│  │ (DoS Detection)  │   │  │  │ Collection       │    │
│  └──────────────────┘   │  │  └──────────────────┘    │
│  ┌──────────────────┐   │  │                          │
│  │ Isolation Forest │   │  │  Stores detected         │
│  │ (Fraud Detection)│   │  │  anomalies for           │
│  └──────────────────┘   │  │  future reference        │
└─────────────────────────┘  └──────────────────────────┘
How Data Flows:

User uploads CSV → Frontend sends file to Backend
Backend receives CSV → Reads and processes the data
ML Models analyze → Check each session for anomalies
Results saved → MongoDB stores all detected anomalies
Frontend displays → User sees dashboard with alerts
User takes action → Can flag users or acknowledge alerts


✨ Features
🔍 Anomaly Detection

Bill Fraud Detection: High energy consumption with minimal payment
DoS Attack Detection: Abnormally short session durations
Multi-User Conflict Detection: Overlapping sessions on same charger

📊 Dashboard Features

Real-time Statistics: Active sessions, critical alerts, warnings
Interactive Tables: Filter by anomaly type
Detailed View: Click any session to see full details
Visual Analytics: Charts and graphs
Alert Management: Flag users, acknowledge alerts
Historical Logs: View past anomaly records from database

🎨 User Interface

Dark Theme: Easy on the eyes
Responsive Design: Works on desktop and tablets
Toast Notifications: Instant feedback
Color-coded Alerts: Red (critical), Amber (warning), Green (normal)


📋 Prerequisites
Before you start, make sure you have these installed on your computer:
Required Software:

Node.js (v18 or higher)

Download: https://nodejs.org/
Check installation: node --version


pnpm (Package manager)

Install: npm install -g pnpm
Check installation: pnpm --version


Python (v3.8 or higher)

Download: https://www.python.org/downloads/
Check installation: python --version


MongoDB (v4.4 or higher)

Download: https://www.mongodb.com/try/download/community
Check installation: mongod --version


Git (optional, for cloning)

Download: https://git-scm.com/downloads



Skills Required:

✅ Basic command line usage
✅ Basic understanding of CSV files
✅ Ability to follow instructions step-by-step


🚀 Installation Guide
Step 1: Download the Project
bash# If you have the project folder
cd C:\ev-anamoly-detection

# OR if cloning from Git
git clone <your-repository-url>
cd ev-anamoly-detection
Step 2: Setup Backend
bash# Navigate to backend folder
cd backend

# Create virtual environment
python -m venv venv

# Activate virtual environment
# For Windows:
venv\Scripts\activate
# For Mac/Linux:
source venv/bin/activate

# Install dependencies
pip install -r requirements.txt

# OR install manually:
pip install fastapi uvicorn python-multipart pymongo scikit-learn pandas numpy
What this does:

Creates an isolated Python environment
Installs all required Python libraries
Keeps your project dependencies separate from system Python

Step 3: Setup Frontend
bash# Navigate to frontend folder (open new terminal)
cd frontend

# Install dependencies
pnpm install
What this does:

Downloads all JavaScript libraries
Sets up React, TypeScript, Tailwind CSS, etc.
Prepares the frontend for development

Step 4: Setup MongoDB
Windows:
bash# Start MongoDB service (as Administrator)
net start MongoDB
Mac/Linux:
bashbrew services start mongodb-community
OR manually:
bashmongod
Verify MongoDB is running:

Open browser: http://localhost:27017
You should see: "It looks like you are trying to access MongoDB over HTTP..."


🎮 How to Run the Project
Terminal 1: Start Backend
bash# Navigate to backend folder
cd C:\ev-anamoly-detection\backend

# Activate virtual environment
venv\Scripts\activate

# Start FastAPI server
python -m uvicorn main:app --reload
```

**You should see:**
```
INFO:     Uvicorn running on http://127.0.0.1:8000
INFO:     Application startup complete.
Test it: Open http://localhost:8000/docs in browser - you'll see API documentation.
Terminal 2: Start Frontend
bash# Navigate to frontend folder
cd C:\ev-anamoly-detection\frontend

# Start development server
pnpm run dev
```

**You should see:**
```
VITE v5.x.x  ready in xxx ms
➜  Local:   http://localhost:5173/
Open it: Go to http://localhost:5173 in your browser.

📖 How to Use the Application
Step 1: Prepare Your CSV File
Create a CSV file with charging session data. Example format:
Option A: Snake Case (Recommended)
csvsession_id,user_id,charger_id,start_time,duration,energy,payment,ip_address
S1001,U123,CH45,10:30:00,120,75.5,0.50,192.168.1.10
S1002,U456,CH12,11:45:00,3,5.2,2.00,192.168.1.11
Option B: Camel Case (Also Supported)
csvsessionId,userId,chargerId,startTime,duration,energy,payment,ipAddress
S1001,U123,CH45,10:30:00,120,75.5,0.50,192.168.1.10
S1002,U456,CH12,11:45:00,3,5.2,2.00,192.168.1.11
```

**Column Descriptions:**
- `session_id`: Unique identifier for the charging session
- `user_id`: ID of the user
- `charger_id`: Which charging station was used
- `start_time`: When charging started
- `duration`: How long charging lasted (minutes)
- `energy`: Electricity consumed (kWh)
- `payment`: Amount paid (₹)
- `ip_address`: Network address (optional)

### Step 2: Upload CSV

1. Open the dashboard: `http://localhost:5173`
2. Click the **"Upload CSV"** button (blue button, top right)
3. Select your CSV file
4. Click "Open"

**What happens:**
- ✅ File is sent to backend
- ✅ ML models analyze the data
- ✅ Anomalies are detected
- ✅ Results are saved to MongoDB
- ✅ Dashboard updates with results

### Step 3: Explore the Dashboard

#### Stats Cards (Top Section)
- **Active Sessions**: Non-critical sessions
- **Total Sessions**: All uploaded sessions
- **Critical Alerts**: High-priority anomalies
- **Warnings**: Medium-priority issues
- **Bill Fraud Detected**: Count of fraud cases
- **DoS Attacks Detected**: Count of DoS attempts
- **Multi-User Conflicts**: Count of conflicts

#### Tabs (Middle Section)
Click different tabs to filter anomalies:
- **All Anomalies**: See everything
- **Fraud**: Only billing fraud cases
- **DoS**: Only DoS attacks
- **Multi-User**: Only conflicts
- **Analytics**: Charts and statistics

#### Anomaly Table
- Click any row to see detailed information
- Color-coded status icons:
  - 🔴 Red X: Critical
  - 🟡 Yellow ⚠️: Warning
  - 🟢 Green ✓: Normal

#### Alert Panel (Right Side)
When you click a session, you'll see:
- **Alert Header**: Type and severity
- **Session Details**: All information about the session
- **Risk Score**: How suspicious it is (0-100%)
- **Energy Usage Chart**: Visual representation
- **Action Buttons**:
  - "Flag User & Suspend Session"
  - "Acknowledge Alert"
  - "View Charger Logs"

### Step 4: View Historical Logs

1. Click **"View Logs"** button (purple button, top right)
2. Click **"Fetch Logs"** in the dialog
3. See all previously detected anomalies from MongoDB
4. Click any log to load it into the dashboard

---

## 📁 Project Structure
```
ev-anamoly-detection/
│
├── backend/                          # Backend API
│   ├── main.py                       # FastAPI application
│   ├── anomaly_detector.py           # ML detection logic
│   ├── dos_model.pkl                 # DoS detection model
│   ├── fraud_model.pkl               # Fraud detection model
│   ├── requirements.txt              # Python dependencies
│   ├── uploads/                      # Uploaded CSV files
│   └── venv/                         # Virtual environment
│
├── frontend/                         # Frontend application
│   ├── public/                       # Static files
│   ├── src/                          # Source code
│   │   ├── components/               # React components
│   │   │   ├── ui/                   # UI components
│   │   │   │   ├── badge.tsx
│   │   │   │   ├── button.tsx
│   │   │   │   ├── card.tsx
│   │   │   │   ├── dialog.tsx
│   │   │   │   ├── input.tsx
│   │   │   │   ├── scroll-area.tsx
│   │   │   │   └── tabs.tsx
│   │   │   ├── AlertPanel.tsx        # Alert details panel
│   │   │   ├── AnomalyCharts.tsx     # Analytics charts
│   │   │   ├── AnomalyTable.tsx      # Data table
│   │   │   ├── EVDashboard.tsx       # Main dashboard
│   │   │   ├── FileUpload.tsx        # CSV upload
│   │   │   ├── LogsViewer.tsx        # MongoDB logs
│   │   │   └── StatsCards.tsx        # Statistics cards
│   │   ├── lib/                      # Utilities
│   │   │   ├── api.ts                # Backend API calls
│   │   │   ├── transformers.ts       # Data transformation
│   │   │   └── utils.ts              # Helper functions
│   │   ├── types/                    # TypeScript types
│   │   │   └── index.ts
│   │   ├── App.tsx                   # Root component
│   │   ├── main.tsx                  # Entry point
│   │   └── index.css                 # Global styles
│   ├── package.json                  # Dependencies
│   ├── tsconfig.json                 # TypeScript config
│   ├── tailwind.config.js            # Tailwind config
│   ├── postcss.config.js             # PostCSS config
│   └── vite.config.ts                # Vite config
│
└── README.md                         # This file
Key Files Explained:
Backend Files:
main.py - Main Backend Application
python# Handles:
# - Receiving CSV uploads
# - Processing files
# - Calling ML models
# - Saving to MongoDB
# - Returning results
anomaly_detector.py - ML Detection Logic
python# Contains:
# - detect_anomalies() function
# - Loads ML models
# - Analyzes each session
# - Returns list of anomalies
```

**`.pkl files`** - Pre-trained Models
```
# Binary files containing:
# - Trained Isolation Forest models
# - Learned patterns of normal behavior
# - Used for predictions
```

#### Frontend Files:

**`EVDashboard.tsx`** - Main Component
- Manages overall state
- Coordinates all other components
- Handles data flow

**`FileUpload.tsx`** - Upload Handler
- Handles file selection
- Sends file to backend
- Shows upload progress

**`AnomalyTable.tsx`** - Data Display
- Shows sessions in table format
- Handles row selection
- Filters by anomaly type

**`AlertPanel.tsx`** - Detail View
- Shows selected session details
- Displays risk score
- Action buttons

**`api.ts`** - Backend Communication
- `uploadAndPredict()`: Upload CSV
- `fetchLogs()`: Get MongoDB data

---

## 🔌 API Documentation

### Base URL
```
http://localhost:8000
Endpoints
1. Upload CSV and Detect Anomalies
Endpoint: POST /predict/
Description: Upload a CSV file, analyze it with ML models, save anomalies to database, and return results.
Request:
httpPOST /predict/
Content-Type: multipart/form-data

file: <CSV_FILE>
Response:
json{
  "filename": "charging_data.csv",
  "total_sessions": 100,
  "anomalies_found": 25,
  "anomalies": [
    {
      "session_id": "S1001",
      "anomaly_type": "billing_fraud",
      "timestamp": "2025-10-26T10:30:00",
      "user_id": "U123",
      "charging_station_id": "CH45",
      "energy_consumed": 75.5,
      "amount_billed": 0.50,
      "duration": 120
    }
  ]
}
Anomaly Types:

"billing_fraud" - High energy, low payment
"dos_attack" - Very short duration
"multi_user_conflict" - Overlapping sessions

2. Fetch Historical Logs
Endpoint: GET /logs/
Description: Retrieve all anomalies stored in MongoDB.
Request:
httpGET /logs/
Response:
json{
  "anomalies": [
    {
      "session_id": "S1001",
      "anomaly_type": "billing_fraud",
      "timestamp": "2025-10-26T10:30:00",
      "user_id": "U123",
      "charging_station_id": "CH45",
      "energy_consumed": 75.5,
      "amount_billed": 0.50,
      "duration": 120
    }
  ]
}

🤖 Machine Learning Models
What is Isolation Forest?
Simple Explanation:
Imagine you have 1000 normal charging sessions and 10 suspicious ones. Isolation Forest is like a smart filter that separates the unusual ones from the normal ones.
How it works:

Training Phase (Already done):

Model learns what "normal" looks like
Studies patterns in clean data
Saves knowledge in .pkl files


Detection Phase (What happens when you upload):

Examines each session
Compares to learned "normal" patterns
Assigns anomaly score (0 to 1)
If score > threshold → Mark as anomaly



Models in This Project:
1. DoS Attack Detection Model (dos_model.pkl)
What it detects:

Sessions with abnormally short duration
Multiple sessions from same user in short time
Pattern of booking but not charging

Features used:

Duration (main feature)
Energy consumed
Time between sessions

Example:
python# Normal session
duration = 120 minutes → Score: 0.1 (Normal)

# DoS attack
duration = 2 minutes → Score: 0.95 (Anomaly!)
2. Fraud Detection Model (fraud_model.pkl)
What it detects:

High energy consumption with low payment
Payment significantly below expected amount
Unusual energy-to-payment ratios

Features used:

Energy consumed
Amount paid
Energy/Payment ratio

Example:
python# Normal session
energy = 50 kWh, payment = ₹400 → Score: 0.2 (Normal)

# Fraud
energy = 75 kWh, payment = ₹0.50 → Score: 0.98 (Anomaly!)
How Detection Works in Code:
pythondef detect_anomalies(df):
    anomalies = []
    
    # Load models
    dos_model = load('dos_model.pkl')
    fraud_model = load('fraud_model.pkl')
    
    for index, row in df.iterrows():
        # Check for DoS
        if row['duration'] < 5:  # Very short
            dos_score = dos_model.predict([[row['duration']]])
            if dos_score > 0.8:
                anomalies.append({
                    'session_id': row['session_id'],
                    'anomaly_type': 'dos_attack',
                    'score': dos_score
                })
        
        # Check for Fraud
        if row['energy'] > 50 and row['payment'] < 1:
            fraud_score = fraud_model.predict([[row['energy'], row['payment']]])
            if fraud_score > 0.8:
                anomalies.append({
                    'session_id': row['session_id'],
                    'anomaly_type': 'billing_fraud',
                    'score': fraud_score
                })
    
    return anomalies

🗄️ Database Schema
MongoDB Database: ev_charging_db
Collection: anomalies
Purpose: Stores all detected anomalies for historical reference.
Document Structure:
json{
  "_id": ObjectId("507f1f77bcf86cd799439011"),
  "session_id": "S1001",
  "anomaly_type": "billing_fraud",
  "timestamp": "2025-10-26T10:30:00.000Z",
  "user_id": "U123",
  "charging_station_id": "CH45",
  "energy_consumed": 75.5,
  "amount_billed": 0.50,
  "duration": 120,
  "ip_address": "192.168.1.10",
  "detected_at": "2025-10-26T15:45:00.000Z"
}
Fields Explained:

_id: MongoDB's unique identifier (auto-generated)
session_id: Your charging session ID
anomaly_type: Type of anomaly detected
timestamp: When the charging session occurred
user_id: User who performed the session
charging_station_id: Which charger was used
energy_consumed: Electricity used (kWh)
amount_billed: Payment amount (₹)
duration: Session length (minutes)
ip_address: Network address (if available)
detected_at: When our system detected this (auto-added)

Query Examples:
View all anomalies:
javascriptdb.anomalies.find()
Find all fraud cases:
javascriptdb.anomalies.find({ anomaly_type: "billing_fraud" })
Count total anomalies:
javascriptdb.anomalies.countDocuments()
Find anomalies by user:
javascriptdb.anomalies.find({ user_id: "U123" })
```

---

## 🐛 Troubleshooting

### Common Issues and Solutions

#### Issue 1: Backend Not Starting

**Error:**
```
ModuleNotFoundError: No module named 'fastapi'
Solution:
bash# Make sure virtual environment is activated
venv\Scripts\activate

# Reinstall dependencies
pip install -r requirements.txt
```

---

#### Issue 2: Frontend Not Starting

**Error:**
```
Error: Cannot find module 'react'
Solution:
bash# Delete node_modules and reinstall
Remove-Item -Recurse -Force node_modules
pnpm install
```

---

#### Issue 3: CORS Error in Browser

**Error:**
```
Access to XMLHttpRequest blocked by CORS policy
Solution:
Ensure your main.py has CORS middleware:
pythonapp.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:5173"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)
```

---

#### Issue 4: MongoDB Not Connecting

**Error:**
```
pymongo.errors.ServerSelectionTimeoutError
Solution:
bash# Windows
net start MongoDB

# Verify it's running
# Open browser: http://localhost:27017
```

---

#### Issue 5: CSV Upload Fails

**Error:**
```
CSV is missing required columns
Solution:
Make sure your CSV has these columns (any format):

session_id (or sessionId)
user_id (or userId)
charger_id (or chargerId)
duration
energy
payment


Issue 6: No Anomalies Detected
Possible Reasons:

Your data is genuinely normal
Thresholds are too high
Models need retraining

Solution:
Test with this sample data (guaranteed to trigger anomalies):
csvsession_id,user_id,charger_id,duration,energy,payment
S1001,U123,CH45,2,5.0,1.00
S1002,U456,CH12,120,85.0,0.50
```

---

#### Issue 7: Port Already in Use

**Error:**
```
Error: Port 8000 is already in use
Solution:
bash# Windows - Find and kill process
netstat -ano | findstr :8000
taskkill /PID <PID> /F

# OR use different port
uvicorn main:app --reload --port 8001

🚀 Future Enhancements
Planned Features:

Real-time Monitoring

WebSocket integration
Live dashboard updates
Real-time alerts


Advanced Analytics

Trend analysis
Predictive maintenance
User behavior patterns


Email Notifications

Alert emails for critical anomalies
Daily/weekly reports
Configurable alerts


User Management

Login/authentication
Role-based access
User profiles


Export Features

Export anomalies to PDF
Generate reports
Excel export


Mobile App

iOS and Android apps
Push notifications
On-the-go monitoring


Advanced ML

Deep learning models
Time series analysis
Automated model retraining


Integration

REST API for third-party
Webhook support
Payment gateway integration




📝 Notes for Developers
Making Changes
Adding New Anomaly Types:

Update Backend (anomaly_detector.py):

pythondef detect_new_anomaly(row):
    if row['new_condition']:
        return {
            'session_id': row['session_id'],
            'anomaly_type': 'new_anomaly_type',
            'score': 0.95
        }

Update Frontend Types (types/index.ts):

typescriptexport interface Anomaly {
  anomaly_type: 'dos_attack' | 'billing_fraud' | 'multi_user_conflict' | 'new_anomaly_type';
}

Add UI Support (in relevant components)

Modifying Thresholds:
Edit anomaly_detector.py:
python# Current thresholds
DOS_DURATION_THRESHOLD = 5  # minutes
FRAUD_PAYMENT_THRESHOLD = 1.0  # rupees
FRAUD_ENERGY_THRESHOLD = 50  # kWh

# Adjust as needed

📞 Support
Getting Help:

Check this README - Most answers are here
Check Troubleshooting section - Common issues covered
Check API Documentation - For integration help
Review code comments - Inline explanations

Project Information:

Version: 1.0.0
Last Updated: October 2025
License: MIT
Status: Production Ready


🎓 Learning Resources
If you want to understand more about the technologies used:
Frontend:

React: https://react.dev/learn
TypeScript: https://www.typescriptlang.org/docs/
Tailwind CSS: https://tailwindcss.com/docs

Backend:

FastAPI: https://fastapi.tiangolo.com/
Python: https://docs.python.org/3/tutorial/

Machine Learning:

Scikit-learn: https://scikit-learn.org/stable/
Isolation Forest: https://scikit-learn.org/stable/modules/generated/sklearn.ensemble.IsolationForest.html

Database:

MongoDB: https://docs.mongodb.com/manual/tutorial/
