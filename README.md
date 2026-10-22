# Praxon Technologies — AI-Based Face Recognition Attendance and Employee Management System

A Flask web application designed for **Praxon Technologies** to automate employee attendance using deep face recognition, track entry/exit logs, manage monthly leaves, and calculate monthly attendance by excluding Sundays and company holidays from regular working days.

---

## 🌟 Key Features

1. **AI Face Recognition Kiosk**: Real-time camera access via browser (`getUserMedia`), deep face detection (**YuNet**) and 128-dimensional facial feature representation (**SFace**) with cosine similarity matching.
2. **Contactless Login & Logout**: Automated attendance recording with entry and exit timestamps, duplicate-entry prevention, and accurate working duration calculation.
3. **Biometric Security & Privacy**: Sensitive facial embeddings are saved outside public static assets in `data/face_data/` with restricted references.
4. **Monthly Attendance Engine (Praxon Formula)**:
   - Dynamic calculation excluding all Sundays in the selected month.
   - Deduction of registered non-Sunday company holidays.
   - $$\text{Regular Working Days} = \text{Calendar Days} - \text{Sundays} - \text{Company Holidays}$$
   - $$\text{Absent Days} = \text{Regular Working Days} - \text{Present Days} - \text{Approved Leave Days}$$
   - Handles mid-month joining dates.
5. **Leave & Holiday Management**: Leave application submission, review/approval workflow, and configurable company holidays calendar.
6. **Executive Reporting**: One-click export of monthly attendance statements to **Microsoft Excel (.xlsx)** via `OpenPyXL` and **PDF** via `ReportLab`.
7. **Database Compatibility**: Primary support for **MySQL** (`PyMySQL`) with transparent fallback to **SQLite** for rapid local deployment without database server configuration.

---

## 📁 Project Structure

```
praxon_attendance/
├── app.py                     # Flask application factory, routes registration & CLI
├── config.py                  # Core configuration, database URIs, paths, & thresholds
├── database.py                # SQLAlchemy models: Admin, Employee, Attendance, Leave, Holiday
├── init_db.py                 # Database initialization & demo seeding script
├── schema.sql                 # MySQL schema DDL definition
├── requirements.txt           # Python dependency specifications
│
├── models/
│   ├── face_model.py          # OpenCV YuNet & SFace deep face recognition engine
│   └── weights/               # Preloaded ONNX weights (YuNet & SFace)
│
├── routes/
│   ├── admin_routes.py        # Authentication & executive dashboard
│   ├── employee_routes.py     # Employee directory & biometric face enrollment
│   ├── attendance_routes.py   # Kiosk terminal, daily logs, & monthly calculations
│   ├── leave_routes.py        # Leaves management & company holidays calendar
│   └── report_routes.py       # Excel (.xlsx) and PDF (.pdf) export endpoints
│
├── services/
│   ├── face_service.py        # Biometric encoding, liveness, & matching
│   ├── attendance_service.py  # Login/logout logic, Sunday exclusion, & monthly calculations
│   └── report_service.py      # OpenPyXL and ReportLab document generators
│
├── templates/                 # Responsive Bootstrap 5 HTML templates
│   ├── base.html
│   ├── login.html
│   ├── dashboard.html
│   ├── employees.html
│   ├── add_employee.html
│   ├── face_registration.html
│   ├── attendance.html        # Live scanner terminal kiosk
│   ├── daily_attendance.html
│   ├── monthly_attendance.html
│   ├── leaves.html
│   ├── holidays.html
│   └── reports.html
│
├── static/
│   ├── css/style.css          # Praxon corporate styles & camera overlays
│   └── js/camera.js           # MediaDevices webcam streaming & biometric capture
│
├── instance/
│   └── config.py              # Optional local credential overrides
│
├── data/
│   └── face_data/             # Secure biometric vector storage (strictly non-public)
│
└── exports/                   # Generated Excel and PDF monthly statements
```

---

## 🚀 Quick Start Guide

### 1. Environment Setup (Anaconda)
Open Anaconda Prompt and activate the environment:
```bash
conda activate praxon
# or use your existing environment with Python 3.11+:
# conda activate 2602
```

Install requirements:
```bash
pip install -r requirements.txt
```

### 2. Database Configuration

#### Option A: MySQL (Production / Standard)
1. Ensure your MySQL server is running (e.g., via XAMPP, WampServer, or native MySQL Service on port `3306`).
2. Run the SQL schema or create the database:
   ```sql
   CREATE DATABASE praxon_attendance;
   ```
3. Set your credentials in `.env` or `instance/config.py`:
   ```ini
   MYSQL_HOST=localhost
   MYSQL_PORT=3306
   MYSQL_USER=root
   MYSQL_PASSWORD=your_password
   MYSQL_DB=praxon_attendance
   ```

#### Option B: SQLite (Zero Configuration)
If MySQL is not currently running, the application automatically falls back to local SQLite (`praxon_attendance.db`). You can also force SQLite by setting:
```ini
USE_SQLITE=true
```

### 3. Initialize & Seed Demo Data
Run the seeding script to create database tables, register default admin credentials, add sample employees, holidays, and benchmark October 2026 attendance data:
```bash
python init_db.py
```

### 4. Run the Web Application
```bash
python app.py
```
Open your browser and navigate to:
- **Admin Dashboard**: `http://127.0.0.1:5000/login`
  - **Username**: `admin`
  - **Password**: `admin123`
- **Attendance Kiosk Terminal**: `http://127.0.0.1:5000/attendance`

---

## 👤 Attendance Scanning Workflow

1. Open `http://127.0.0.1:5000/attendance` on any device equipped with a camera.
2. Grant camera access when prompted by the browser.
3. Stand in front of the camera with your face aligned within the oval guide.
4. Click **RECORD LOGIN** at the start of your shift:
   - The system captures the frame, identifies the employee via Deep SFace cosine similarity, verifies that no login has been recorded yet for the day, and marks the employee as Present.
5. Click **RECORD LOGOUT** at the end of your shift:
   - The system identifies the employee, calculates the net working hours ($$T_{\text{logout}} - T_{\text{login}}$$), and updates the record with the shift status (e.g. Present or Half Day).

---

## 📊 Monthly Attendance Calculation Example

For October 2026:
- **Total Calendar Days**: 31
- **Sundays Excluded**: 4 (Oct 4, 11, 18, 25)
- **Company Holidays**: 1 (Gandhi Jayanti, Oct 2)
- **Regular Working Days**: $31 - 4 - 1 = 26$ (or 27 if 0 additional holidays)
- **Present Days**: 23
- **Approved Leaves**: 2
- **Absent Days**: $26 - 23 - 2 = 1$ absent day

Reports can be exported instantly to `.xlsx` or `.pdf` from the **Reports** or **Monthly Calculation** menus.
