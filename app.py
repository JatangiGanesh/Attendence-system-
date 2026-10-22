import os
from pathlib import Path
from flask import Flask, redirect, url_for
from flask_login import LoginManager
from sqlalchemy import text
from sqlalchemy.exc import OperationalError

from config import Config
from database import db, Admin, Employee, Attendance, Leave, Holiday

def create_app(config_class=Config):
    app = Flask(__name__, instance_relative_config=True)
    app.config.from_object(config_class)

    # Load instance overrides if exists
    try:
        app.config.from_pyfile("config.py", silent=True)
    except Exception:
        pass

    # Ensure storage paths exist
    app.config["FACE_DATA_DIR"].mkdir(parents=True, exist_ok=True)
    app.config["EXPORTS_DIR"].mkdir(parents=True, exist_ok=True)

    # Verify database connection; fallback to SQLite if MySQL is unavailable
    if not app.config.get("USE_SQLITE", False):
        try:
            # Test direct connection
            import pymysql
            conn = pymysql.connect(
                host=app.config.get("MYSQL_HOST", "localhost"),
                user=app.config.get("MYSQL_USER", "root"),
                password=app.config.get("MYSQL_PASSWORD", ""),
                port=app.config.get("MYSQL_PORT", 3306),
                connect_timeout=2
            )
            # Ensure database exists
            with conn.cursor() as cursor:
                cursor.execute(f"CREATE DATABASE IF NOT EXISTS `{app.config.get('MYSQL_DB', 'praxon_attendance')}` CHARACTER SET utf8mb4;")
            conn.commit()
            conn.close()
        except Exception as e:
            print(f"[Database Notification] Could not connect to MySQL server ({e}).")
            print(f"[Database Notification] Falling back seamlessly to local SQLite: {app.config['SQLITE_URI']}")
            app.config["SQLALCHEMY_DATABASE_URI"] = app.config["SQLITE_URI"]

    db.init_app(app)

    # Login Manager
    login_manager = LoginManager()
    login_manager.login_view = "admin.login"
    login_manager.login_message = "Please log in to access the administrator portal."
    login_manager.login_message_category = "warning"
    login_manager.init_app(app)

    @login_manager.user_loader
    def load_user(user_id):
        return Admin.query.get(int(user_id))

    # Register Blueprints
    from routes.admin_routes import admin_bp
    from routes.employee_routes import employee_bp
    from routes.attendance_routes import attendance_bp
    from routes.leave_routes import leave_bp
    from routes.report_routes import report_bp

    app.register_blueprint(admin_bp)
    app.register_blueprint(employee_bp)
    app.register_blueprint(attendance_bp)
    app.register_blueprint(leave_bp)
    app.register_blueprint(report_bp)

    @app.context_processor
    def inject_global_data():
        from datetime import datetime
        return {
            "current_year": datetime.now().year,
            "company_name": "Praxon Technologies"
        }

    # Initialize tables and default admin if not created
    with app.app_context():
        try:
            db.create_all()
            if not Admin.query.first():
                default_admin = Admin(
                    username="admin",
                    email="admin@praxon.com",
                    full_name="Praxon System Admin",
                    is_active_account=True
                )
                default_admin.set_password("admin123")
                db.session.add(default_admin)
                db.session.commit()
                print("[Praxon System] Default administrator initialized: Username 'admin', Password 'admin123'")
        except Exception as err:
            print(f"[Database Initialization Warning] {err}")

    return app

if __name__ == "__main__":
    app = create_app()
    print("=====================================================================")
    print(" Praxon Technologies Face Recognition Attendance & Management System")
    print(" Running at http://127.0.0.1:5000")
    print(" Admin Credentials: username: admin | password: admin123")
    print("=====================================================================")
    app.run(host="0.0.0.0", port=5000, debug=True)
