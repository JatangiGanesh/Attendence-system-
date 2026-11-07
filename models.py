from datetime import datetime
from flask_sqlalchemy import SQLAlchemy
from werkzeug.security import generate_password_hash, check_password_hash

db = SQLAlchemy()

class Donor(db.Model):
    __tablename__ = 'donors'
    
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    mobile = db.Column(db.String(15), nullable=False, unique=True, index=True)
    email = db.Column(db.String(120), nullable=True)
    organization = db.Column(db.String(150), nullable=True)
    password_hash = db.Column(db.String(255), nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    
    events = db.relationship('AnnadanamEvent', backref='donor', lazy=True, cascade="all, delete-orphan")

    def set_password(self, password):
        self.password_hash = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.password_hash, password)


class AnnadanamEvent(db.Model):
    __tablename__ = 'annadanam_events'
    
    id = db.Column(db.Integer, primary_key=True)
    donor_id = db.Column(db.Integer, db.ForeignKey('donors.id'), nullable=True)
    
    # Donor Information (kept on event too for fast query and guest submissions)
    donor_name = db.Column(db.String(100), nullable=False)
    mobile_number = db.Column(db.String(15), nullable=False, index=True)
    whatsapp_number = db.Column(db.String(15), nullable=True)
    organization_pandal = db.Column(db.String(150), nullable=True) # e.g. "Balaji Nagar Ganesh Youth Club"
    
    # Food Details
    food_category = db.Column(db.String(50), default="Full Meals Prasadam") # Full Meals, Pulihara & Pongali, Sweets, etc.
    food_details = db.Column(db.Text, nullable=False) # e.g. "Sambar Rice, Curd Rice, Bellam Pongali, Laddu, Banana"
    available_quantity = db.Column(db.String(100), nullable=False) # e.g. "500 Plates", "1000 Devotees", "Unlimited"
    special_notes = db.Column(db.String(255), nullable=True) # e.g. "Seating dining available, clean drinking water provided"
    
    # Schedule Details
    festival_day = db.Column(db.String(20), nullable=False, default="Day 1") # Day 1 to Day 9 or All 9 Days
    event_date = db.Column(db.String(20), nullable=False) # YYYY-MM-DD
    distribution_timings = db.Column(db.String(100), nullable=False) # e.g. "12:30 PM - 3:30 PM & 7:30 PM - 9:30 PM"
    
    # Location Details
    state = db.Column(db.String(50), default="Telangana")
    district = db.Column(db.String(100), nullable=False, index=True) # e.g. Hyderabad, Visakhapatnam, Vijayawada
    village_mandal = db.Column(db.String(100), nullable=False, index=True) # e.g. Dilsukhnagar, Gajuwaka, Benz Circle
    complete_address = db.Column(db.Text, nullable=False)
    landmark = db.Column(db.String(150), nullable=True)
    google_maps_url = db.Column(db.String(500), nullable=True)
    latitude = db.Column(db.Float, nullable=True)
    longitude = db.Column(db.Float, nullable=True)
    
    # Status & Management
    status = db.Column(db.String(30), default="Available") # Available, Serving Now, Exhausted, Completed
    is_verified = db.Column(db.Boolean, default=True) # Default True for instant visibility, can be toggled by Admin
    is_featured = db.Column(db.Boolean, default=False)
    views_count = db.Column(db.Integer, default=0)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    def to_dict(self):
        return {
            'id': self.id,
            'donor_name': self.donor_name,
            'mobile_number': self.mobile_number,
            'whatsapp_number': self.whatsapp_number,
            'organization_pandal': self.organization_pandal,
            'food_category': self.food_category,
            'food_details': self.food_details,
            'available_quantity': self.available_quantity,
            'festival_day': self.festival_day,
            'event_date': self.event_date,
            'distribution_timings': self.distribution_timings,
            'district': self.district,
            'village_mandal': self.village_mandal,
            'complete_address': self.complete_address,
            'landmark': self.landmark,
            'google_maps_url': self.google_maps_url or f"https://www.google.com/maps/search/?api=1&query={self.latitude},{self.longitude}" if self.latitude else f"https://www.google.com/maps/search/?api=1&query={self.complete_address},+{self.village_mandal},+{self.district}",
            'latitude': self.latitude,
            'longitude': self.longitude,
            'status': self.status,
            'is_verified': self.is_verified,
            'is_featured': self.is_featured,
            'created_at': self.created_at.strftime('%Y-%m-%d %H:%M') if self.created_at else ''
        }


class AdminUser(db.Model):
    __tablename__ = 'admin_users'
    
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(50), unique=True, nullable=False)
    password_hash = db.Column(db.String(255), nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

    def set_password(self, password):
        self.password_hash = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.password_hash, password)
