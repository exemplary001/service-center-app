# Service Center Call Tracker

A simple Service Center Call Tracking application built using FastAPI, SQLAlchemy, HTML, CSS, and JavaScript.

## Features

* Login Authentication
* Dashboard
* Customer Management
* Add Customer
* Edit Customer
* Delete Customer
* Search by Customer Name
* Search by Phone Number
* Pending Call Calculation
* Excel Export
* SQLite or PostgreSQL Database
* Session Authentication
* Auto Import Sample Excel Data
* Single Command Startup

---

# Project Structure

```text
service-center-app/
│
├── HANIF.xlsx
├── main.py
├── requirements.txt
├── .env
│
├── database/
│   └── service_center.db
│
├── app/
│   ├── database.py
│   ├── models.py
│   ├── schemas.py
│   ├── crud.py
│   ├── auth.py
│   │
│   ├── routers/
│   │   ├── auth.py
│   │   ├── dashboard.py
│   │   └── customers.py
│   │
│   └── services/
│       ├── excel_export.py
│       └── excel_import.py
│
├── templates/
│   ├── login.html
│   ├── dashboard.html
│   └── customers.html
│
└── static/
    ├── css/
    │   └── style.css
    │
    ├── js/
    │   └── customers.js
    │
    └── images/
```

---

# Prerequisites

* Python 3.10 or newer
* pip

Verify installation:

```bash
python --version
pip --version
```

---

# Installation

## 1. Clone or Download Project

Place the project folder anywhere on your system.

Example:

```text
C:\Projects\service-center-app
```

---

## 2. Create Virtual Environment

### Windows

```bash
python -m venv venv
venv\Scripts\activate
```

### Linux

```bash
python3 -m venv venv
source venv/bin/activate
```

---

## 3. Install Dependencies

```bash
pip install -r requirements.txt
```

---

# Environment Configuration

Create a file named `.env` in the project root.

Example:

```env
APP_NAME=Service Center Call Tracker

DATABASE_URL=sqlite:///database/service_center.db

LOAD_SAMPLE_DATA=true

SECRET_KEY=change_this_to_a_long_random_secret_key

ADMIN_USERNAME=admin

ADMIN_PASSWORD=admin123

SESSION_COOKIE_NAME=service_center_session
```

For Render Free, use an external PostgreSQL database such as Neon and set `DATABASE_URL`
to the connection string from that database:

```env
DATABASE_URL=postgresql://user:password@host/dbname?sslmode=require
LOAD_SAMPLE_DATA=false
```

Do not use SQLite for live customer data on Render Free because Render's free web
service filesystem is not persistent across redeploys and restarts.

---

# Sample Data Import

Place the Excel file:

```text
HANIF.xlsx
```

in the project root.

Example:

```text
service-center-app/
│
├── HANIF.xlsx
├── main.py
```

If `LOAD_SAMPLE_DATA=true`, the application imports the sample customer data
automatically on startup when the customer table is empty. Set it to `false` on
production hosts such as Render.

---

# Running the Application

Start the application using:

```bash
python main.py
```

The application will start on:

```text
http://localhost:8000
```

---

# Login Credentials

Default credentials:

```text
Username: admin
Password: admin123
```

---

# First-Time Database Reset

If you want to re-import data from Excel:

### Windows

```powershell
del database\service_center.db
```

### Linux

```bash
rm database/service_center.db
```

Then restart:

```bash
python main.py
```

---

# Application Workflow

1. Open Login Page
2. Login using Admin Credentials
3. Dashboard opens
4. Click "Manage Customers"
5. Add/Edit/Delete Customers
6. Search Customers
7. Export Data to Excel

---

# Dashboard

Dashboard displays:

* Total Customers
* Today's Calls
* Today's Closed Calls
* Today's Pending Calls

---

# Customer Module

Customer fields:

* Customer Name
* Address
* Phone Number
* Date
* Total Calls
* Closed Calls

Pending Calls are calculated automatically:

```text
Pending Calls = Total Calls - Closed Calls
```

---

# Excel Export

Click:

```text
Export Excel
```

A file named:

```text
customer_report.xlsx
```

will be downloaded.

---

# Troubleshooting

## Port Already In Use

If port 8000 is already occupied:

```bash
netstat -ano | findstr :8000
```

Terminate the process or change the port in `main.py`.

---

## Database Not Created

Ensure the database folder exists:

```text
database/
```

---

## Module Not Found

Reinstall dependencies:

```bash
pip install -r requirements.txt
```

---

## Login Not Working

Verify `.env` values:

```env
ADMIN_USERNAME=admin
ADMIN_PASSWORD=admin123
```

Delete database and restart if required.

---

# Technology Stack

Backend:

* FastAPI
* SQLAlchemy
* SQLite / PostgreSQL

Frontend:

* HTML
* CSS
* JavaScript
* Bootstrap 5

Excel Handling:

* OpenPyXL
* Pandas

Authentication:

* Session Middleware
* Passlib (bcrypt)

---

# Startup Command

```bash
python main.py
```
