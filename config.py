import os

BASE_DIR = os.path.abspath(os.path.dirname(__file__))

class Config:
    SECRET_KEY = os.environ.get('SECRET_KEY', 'vinayaka-chavithi-annadanam-blessings-2026-secret-key')
    # Default to SQLite for zero-setup execution, switchable to MySQL via DATABASE_URL
    # MySQL Example: mysql+pymysql://username:password@localhost:3306/annadanam_db
    SQLALCHEMY_DATABASE_URI = os.environ.get(
        'DATABASE_URL', 
        f"sqlite:///{os.path.join(BASE_DIR, 'annadanam.db')}"
    )
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    SQLALCHEMY_ENGINE_OPTIONS = {
        'pool_recycle': 280,
    } if 'mysql' in os.environ.get('DATABASE_URL', '') else {}
    
    # App Settings
    FESTIVAL_NAME = "Vinayaka Chavithi 9 Days Annadanam Finder"
    ADMIN_DEFAULT_USERNAME = os.environ.get('ADMIN_USER', 'admin')
    ADMIN_DEFAULT_PASSWORD = os.environ.get('ADMIN_PASS', 'admin123')
