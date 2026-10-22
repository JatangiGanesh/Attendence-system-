import os
from pathlib import Path
from dotenv import load_dotenv

BASE_DIR = Path(__file__).resolve().parent
load_dotenv(BASE_DIR / ".env")

class Config:
    SECRET_KEY = os.getenv("SECRET_KEY", "praxon-technologies-attendance-super-secret-key-2026")
    
    # Database configuration
    MYSQL_HOST = os.getenv("MYSQL_HOST", "localhost")
    MYSQL_PORT = int(os.getenv("MYSQL_PORT", 3306))
    MYSQL_USER = os.getenv("MYSQL_USER", "root")
    MYSQL_PASSWORD = os.getenv("MYSQL_PASSWORD", "")
    MYSQL_DB = os.getenv("MYSQL_DB", "praxon_attendance")

    # Primary MySQL URI
    SQLALCHEMY_DATABASE_URI = os.getenv(
        "DATABASE_URL",
        f"mysql+pymysql://{MYSQL_USER}:{MYSQL_PASSWORD}@{MYSQL_HOST}:{MYSQL_PORT}/{MYSQL_DB}"
    )
    
    # Fallback to SQLite if MySQL is unavailable or USE_SQLITE is set
    USE_SQLITE = os.getenv("USE_SQLITE", "false").lower() in ("true", "1", "t")
    SQLITE_URI = f"sqlite:///{BASE_DIR / 'praxon_attendance.db'}"
    
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    SQLALCHEMY_ENGINE_OPTIONS = {
        "pool_recycle": 280,
        "pool_pre_ping": True,
    }

    # Secure storage directories (strictly OUTSIDE of static folder)
    FACE_DATA_DIR = BASE_DIR / "data" / "face_data"
    EXPORTS_DIR = BASE_DIR / "exports"

    # Attendance business logic defaults
    WORK_DAY_HOURS = 8.0
    FACE_SIMILARITY_THRESHOLD = 0.55  # For face cosine similarity / distance
