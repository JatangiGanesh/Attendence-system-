# 🕉️ Vinayaka Chavithi 9 Days Annadanam Information and Location Finder
### *అన్నదాత సుఖీభవ (Annadata Sukhibhava) — Service to humanity is service to Lord Vinayaka*

A full-stack web application designed to connect generous food donors, temple trusts, and Ganesh Utsav Samithis with devotees and people seeking Mahaprasadam during the auspicious nine days of Vinayaka Chavithi celebrations.

---

## 🌟 Key Highlights & Features

### 🍛 For Donors, Mandapams & Organizations:
- **Easy Event Registration**: Donors can register and publish Annadanam events with:
  - Donor / Organization name
  - Contact number & WhatsApp number
  - Food menu details (e.g. Sambar Rice, Tamarind Pulihara, Bellam Pongali, Laddu)
  - Estimated available quantity (e.g., 500 plates, 2,000 devotees)
  - Festival Day (Day 1: Chavithi through Day 9: Navami / Maha Prasadam)
  - Distribution timings (e.g. 12:30 PM - 3:30 PM, 7:00 PM - 9:30 PM)
  - State, District, Mandal/Village, complete street address & landmark
  - Google Maps location link with one-click **GPS Geolocation detection**
- **Donor Dashboard**: Donors can log in to update live operational status in real time (`Available`, `Serving Now` with green pulsing radar, `Food Exhausted`, `Completed`).

### 🗺️ For Devotees & Visitors:
- **Interactive Leaflet / OpenStreetMap Visualizer**: View all food distribution points with custom festive pins. Clicking any pin shows the pandal name, menu, and a **"Get Directions"** button.
- **Instant Search & Multi-Filters**: Filter events by:
  - District / City (e.g. Hyderabad, Visakhapatnam, Vijayawada, Guntur, Warangal, Tirupati)
  - Village, Mandal or Landmark keyword
  - Festival Day (Day 1 through Day 9)
  - Food Category (Full Meals Prasadam, Pulihara & Pongali, Tiffin, Sweets)
  - Real-time status (Serving Now, Available)
- **1-Click Google Maps Navigation**: Direct button to launch Google Maps turn-by-turn directions to reach the food counter.
- **Direct Contact & WhatsApp Sharing**: Instant "Call Donor", "WhatsApp Organizer", and "Share Location" buttons.

### 🛡️ For Administrators:
- **Admin Moderation Dashboard**: Accessible at `/admin/login` (Default demo credentials: `admin` / `admin123`).
- Review, verify, feature, or delete donor submissions.
- Real-time analytics of active centers, verified locations, and total devotee reach.

---

## 🛠️ Technology Stack

| Layer | Technologies |
|---|---|
| **Frontend** | HTML5, CSS3, JavaScript (ES6+), Bootstrap 5.3.2, FontAwesome 6, Leaflet.js |
| **Backend** | Python Flask, Jinja2 templating, Werkzeug Security |
| **Database** | SQLite (Default out-of-the-box) / MySQL (Fully supported via SQLAlchemy & PyMySQL) |

---

## 📁 Project Directory Structure

```
annadanam-finder/
├── app.py                  # Main Flask application & routes (Public, Donor, Admin, API)
├── models.py               # SQLAlchemy database models (Donor, AnnadanamEvent, AdminUser)
├── config.py               # App configuration & MySQL / SQLite connection strings
├── seed_data.py            # Pre-populates 9 days of realistic Annadanam events & donors
├── test_app.py             # Route verification and health test suite
├── requirements.txt        # Python package dependencies
├── annadanam.db            # SQLite database file (created automatically)
├── templates/
│   ├── base.html           # Base layout with festive theme, navbar, flashes, footer
│   ├── index.html          # Homepage (Hero, 9-Day pills, Search bar, Leaflet map, Featured cards)
│   ├── events.html         # Full directory search with multi-filters
│   ├── event_detail.html   # Detailed event view with directions, phone, WhatsApp share
│   ├── submit_annadanam.html # Donor event registration form with GPS detection
│   ├── donor_register.html # Donor account creation
│   ├── donor_login.html    # Donor sign in
│   ├── donor_dashboard.html# Donor control panel to update live food status
│   ├── about.html          # Significance of 9 Days Navaratri & Annadanam guidelines
│   └── admin/
│       ├── login.html      # Admin login page
│       └── dashboard.html  # Moderation dashboard (verify, feature, delete)
└── static/
    ├── css/
    │   └── style.css       # Custom festive saffron & gold styles, animations, card styles
    └── js/
        ├── main.js         # GPS auto-detect, share handler, tooltips
        └── map.js          # Leaflet map pins, bounds auto-fit, and popups
```

---

## 🚀 Quick Start Guide

### 1. Navigate to the project folder
```powershell
cd "C:\Users\Jatangi Ganesh\.gemini\antigravity\scratch\annadanam-finder"
```

### 2. Install dependencies (if in a fresh environment)
```powershell
python -m pip install -r requirements.txt
```

### 3. Initialize & Seed Sample Data
```powershell
python seed_data.py
```
*(Pre-configures default admin `admin / admin123` and 8 events across Day 1 to Day 9 in Hyderabad, Vizag, Vijayawada, Warangal, Tirupati, Guntur)*

### 4. Run the Web Server
```powershell
python app.py
```
Open your browser and visit: **`http://localhost:5000`**

---

## 🗄️ Optional: Connecting to MySQL

To switch from SQLite to MySQL:
1. Create a database in MySQL:
   ```sql
   CREATE DATABASE annadanam_db CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci;
   ```
2. Set the `DATABASE_URL` environment variable before running `app.py`:
   ```powershell
   $env:DATABASE_URL="mysql+pymysql://root:YOUR_PASSWORD@localhost:3306/annadanam_db"
   python seed_data.py
   python app.py
   ```

---

## 🔑 Default Credentials

- **Admin Portal**: [http://localhost:5000/admin/login](http://localhost:5000/admin/login)
  - **Username**: `admin`
  - **Password**: `admin123`
- **Sample Donor Account**: [http://localhost:5000/donor/login](http://localhost:5000/donor/login)
  - **Mobile**: `9848022334`
  - **Password**: `donor123`
