from datetime import date, time, datetime, timedelta
from app import create_app
from database import db, Admin, Employee, Attendance, Leave, Holiday

def seed_database():
    app = create_app()
    with app.app_context():
        print("Creating all database tables...")
        db.create_all()

        # 1. Admin
        admin = Admin.query.filter_by(username="admin").first()
        if not admin:
            admin = Admin(
                username="admin",
                email="admin@praxon.com",
                full_name="Praxon System Admin",
                is_active_account=True
            )
            admin.set_password("admin123")
            db.session.add(admin)
            print("Admin user created (Username: admin, Password: admin123)")

        # 2. Company Holidays
        sample_holidays = [
            (date(2026, 1, 26), "Republic Day", "National Holiday"),
            (date(2026, 8, 15), "Independence Day", "National Holiday"),
            (date(2026, 10, 2), "Gandhi Jayanti", "National Holiday"),
            (date(2026, 11, 8), "Diwali", "Festival Holiday"),
            (date(2026, 12, 25), "Christmas", "Festival Holiday"),
        ]
        for h_date, h_name, h_desc in sample_holidays:
            if not Holiday.query.filter_by(holiday_date=h_date).first():
                db.session.add(Holiday(holiday_date=h_date, holiday_name=h_name, holiday_type="Company", description=h_desc))
        print("Company holidays verified.")

        # 3. Sample Employees
        sample_employees = [
            ("PRX-001", "Aarav Sharma", "AI Research", "Lead Computer Vision Engineer", "aarav.sharma@praxon.com", "+91 9876543210", date(2024, 1, 15)),
            ("PRX-002", "Priya Nair", "Software Engineering", "Senior Full-Stack Developer", "priya.nair@praxon.com", "+91 9876543211", date(2024, 3, 1)),
            ("PRX-003", "Rohan Mehta", "DevOps & Cloud", "Cloud Infrastructure Engineer", "rohan.mehta@praxon.com", "+91 9876543212", date(2024, 6, 10)),
            ("PRX-004", "Ananya Verma", "Human Resources", "HR Operations Manager", "ananya.verma@praxon.com", "+91 9876543213", date(2023, 11, 20)),
            ("PRX-005", "Vikram Patel", "Quality Assurance", "QA Automation Lead", "vikram.patel@praxon.com", "+91 9876543214", date(2025, 2, 1)),
        ]

        for emp_id, name, dept, desig, email, phone, joining in sample_employees:
            if not Employee.query.get(emp_id):
                emp = Employee(
                    employee_id=emp_id,
                    employee_name=name,
                    department=dept,
                    designation=desig,
                    email=email,
                    phone=phone,
                    joining_date=joining,
                    status="Active"
                )
                db.session.add(emp)
        print("Sample employees verified.")
        db.session.commit()

        # 4. Seed sample attendance for October 2026 matching the prompt's example:
        # Prompt Example: October 2026 (31 calendar days, 4 Sundays, 27 working days, 23 present, 2 leaves, 2 absent)
        # Let's seed this for PRX-001 (Aarav Sharma)
        emp1 = Employee.query.get("PRX-001")
        if emp1 and not Attendance.query.filter_by(employee_id="PRX-001", attendance_date=date(2026, 10, 1)).first():
            print("Seeding October 2026 attendance benchmark data for PRX-001...")
            # October 2026: Day 1 is Thursday, Oct 2 is Gandhi Jayanti (holiday), Sundays are Oct 4, 11, 18, 25.
            # Let's add 2 approved leave days on Oct 15 & Oct 16
            leave = Leave(
                employee_id="PRX-001",
                start_date=date(2026, 10, 15),
                end_date=date(2026, 10, 16),
                leave_type="Casual Leave",
                reason="Family function",
                approval_status="Approved"
            )
            db.session.add(leave)

            # Add attendances for working days
            present_counter = 0
            for day in range(1, 32):
                d = date(2026, 10, day)
                # Skip Sundays
                if d.weekday() == 6:
                    continue
                # Skip Gandhi Jayanti
                if d == date(2026, 10, 2):
                    continue
                # Skip leave days
                if d in (date(2026, 10, 15), date(2026, 10, 16)):
                    continue

                # We want 23 present days and 2 absent days out of regular working days
                if present_counter < 23:
                    att = Attendance(
                        employee_id="PRX-001",
                        attendance_date=d,
                        login_time=time(9, 15),
                        logout_time=time(18, 0),
                        working_hours=8.75,
                        status="Present"
                    )
                    db.session.add(att)
                    present_counter += 1
                else:
                    # Absent days (no attendance record or marked absent)
                    pass

            # Today's attendance for demo (Oct 15)
            today_att = Attendance.query.filter_by(employee_id="PRX-002", attendance_date=date.today()).first()
            if not today_att:
                db.session.add(Attendance(
                    employee_id="PRX-002",
                    attendance_date=date.today(),
                    login_time=time(9, 10),
                    status="Present"
                ))

            db.session.commit()
            print("Seeding complete successfully!")

if __name__ == "__main__":
    seed_database()
