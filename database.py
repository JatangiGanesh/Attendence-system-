from datetime import datetime, date, time
from flask_sqlalchemy import SQLAlchemy
from flask_login import UserMixin
from werkzeug.security import generate_password_hash, check_password_hash

db = SQLAlchemy()

class Admin(UserMixin, db.Model):
    __tablename__ = "admins"

    admin_id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    username = db.Column(db.String(80), unique=True, nullable=False, index=True)
    email = db.Column(db.String(120), unique=True, nullable=False)
    password_hash = db.Column(db.String(255), nullable=False)
    full_name = db.Column(db.String(100), nullable=False, default="Administrator")
    is_active_account = db.Column(db.Boolean, default=True)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    last_login = db.Column(db.DateTime, nullable=True)

    def get_id(self):
        return str(self.admin_id)

    @property
    def is_active(self):
        return self.is_active_account

    def set_password(self, password: str):
        self.password_hash = generate_password_hash(password)

    def check_password(self, password: str) -> bool:
        return check_password_hash(self.password_hash, password)

    def __repr__(self):
        return f"<Admin {self.username}>"


class Employee(db.Model):
    __tablename__ = "employees"

    employee_id = db.Column(db.String(50), primary_key=True)
    employee_name = db.Column(db.String(100), nullable=False, index=True)
    department = db.Column(db.String(100), nullable=False)
    designation = db.Column(db.String(100), nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    phone = db.Column(db.String(20), nullable=False)
    joining_date = db.Column(db.Date, nullable=False, default=date.today)
    face_data_reference = db.Column(db.String(255), nullable=True)
    status = db.Column(db.String(20), nullable=False, default="Active")  # 'Active' or 'Inactive'
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

    # Relationships
    attendances = db.relationship("Attendance", backref="employee", cascade="all, delete-orphan", lazy="dynamic")
    leaves = db.relationship("Leave", backref="employee", cascade="all, delete-orphan", lazy="dynamic")

    @property
    def has_registered_face(self) -> bool:
        return bool(self.face_data_reference)

    def __repr__(self):
        return f"<Employee {self.employee_id}: {self.employee_name}>"


class Attendance(db.Model):
    __tablename__ = "attendance"

    attendance_id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    employee_id = db.Column(db.String(50), db.ForeignKey("employees.employee_id", ondelete="CASCADE"), nullable=False, index=True)
    attendance_date = db.Column(db.Date, nullable=False, default=date.today, index=True)
    login_time = db.Column(db.Time, nullable=True)
    logout_time = db.Column(db.Time, nullable=True)
    working_hours = db.Column(db.Float, default=0.0)
    status = db.Column(db.String(30), nullable=False, default="Present")  # 'Present', 'Half Day', 'Late', 'Incomplete'
    notes = db.Column(db.String(255), nullable=True)

    __table_args__ = (
        db.UniqueConstraint("employee_id", "attendance_date", name="uq_emp_attendance_date"),
    )

    def calculate_hours(self):
        """Calculate working hours from login and logout times."""
        if self.login_time and self.logout_time:
            # combine with dummy date for delta calculation
            d = date.today()
            dt_in = datetime.combine(d, self.login_time)
            dt_out = datetime.combine(d, self.logout_time)
            delta = dt_out - dt_in
            hours = max(0.0, round(delta.total_seconds() / 3600.0, 2))
            self.working_hours = hours
            if hours >= 7.5:
                self.status = "Present"
            elif hours >= 4.0:
                self.status = "Half Day"
            else:
                self.status = "Short Hours"
            return hours
        return 0.0

    def __repr__(self):
        return f"<Attendance emp={self.employee_id} date={self.attendance_date} hrs={self.working_hours}>"


class Leave(db.Model):
    __tablename__ = "leaves"

    leave_id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    employee_id = db.Column(db.String(50), db.ForeignKey("employees.employee_id", ondelete="CASCADE"), nullable=False, index=True)
    start_date = db.Column(db.Date, nullable=False)
    end_date = db.Column(db.Date, nullable=False)
    leave_type = db.Column(db.String(50), nullable=False)  # 'Casual Leave', 'Sick Leave', 'Paid Leave', etc.
    reason = db.Column(db.Text, nullable=False)
    approval_status = db.Column(db.String(20), nullable=False, default="Pending")  # 'Pending', 'Approved', 'Rejected'
    applied_on = db.Column(db.DateTime, default=datetime.utcnow)
    reviewed_at = db.Column(db.DateTime, nullable=True)
    review_remarks = db.Column(db.String(255), nullable=True)

    @property
    def total_days(self) -> int:
        if self.start_date and self.end_date:
            return max(1, (self.end_date - self.start_date).days + 1)
        return 0

    def __repr__(self):
        return f"<Leave {self.leave_id} emp={self.employee_id} status={self.approval_status}>"


class Holiday(db.Model):
    __tablename__ = "holidays"

    holiday_id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    holiday_date = db.Column(db.Date, unique=True, nullable=False, index=True)
    holiday_name = db.Column(db.String(100), nullable=False)
    holiday_type = db.Column(db.String(50), nullable=False, default="Company")  # 'Company' or 'Weekly'
    description = db.Column(db.String(255), nullable=True)

    def __repr__(self):
        return f"<Holiday {self.holiday_name} on {self.holiday_date}>"
