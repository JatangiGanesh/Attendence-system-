from flask import Flask, render_template, request, redirect, url_for, flash, jsonify, session
from datetime import datetime, date
import os
from functools import wraps

from config import Config
from models import db, Donor, AnnadanamEvent, AdminUser

app = Flask(__name__)
app.config.from_object(Config)
db.init_app(app)

# Helper decorator for Admin authentication
def admin_required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if 'admin_id' not in session:
            flash('Please log in with admin credentials to access the admin dashboard.', 'warning')
            return redirect(url_for('admin_login', next=request.url))
        return f(*args, **kwargs)
    return decorated_function

# Helper decorator for Donor authentication
def donor_required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if 'donor_id' not in session:
            flash('Please sign in to access your donor dashboard.', 'info')
            return redirect(url_for('donor_login', next=request.url))
        return f(*args, **kwargs)
    return decorated_function

@app.context_processor
def inject_global_data():
    # Festival days list for dropdowns and navigation
    days_list = [
        {"day": "Day 1", "title": "Vinayaka Chavithi (Prathishta)"},
        {"day": "Day 2", "title": "Dwitiya (Modaka Pooja)"},
        {"day": "Day 3", "title": "Tritiya (Siddhi Vinayaka)"},
        {"day": "Day 4", "title": "Chaturthi (Ganesh Pooja)"},
        {"day": "Day 5", "title": "Panchami (Vakratunda Archana)"},
        {"day": "Day 6", "title": "Shashti (Vigneshwara Seva)"},
        {"day": "Day 7", "title": "Saptami (Gajanana Homam)"},
        {"day": "Day 8", "title": "Ashtami (Maha Prasadam)"},
        {"day": "Day 9", "title": "Navami (Maha Annadanam & Nimajjanam)"},
        {"day": "All 9 Days", "title": "Daily Continuous Annadanam"}
    ]
    popular_districts = [
        "Hyderabad", "Rangareddy", "Medchal", "Warangal", "Karimnagar", 
        "Nizamabad", "Khammam", "Visakhapatnam", "Vijayawada (NTR)", 
        "Guntur", "Tirupati", "Nellore", "Kurnool", "East Godavari", "West Godavari"
    ]
    return dict(
        festival_days=days_list,
        popular_districts=popular_districts,
        current_year=datetime.now().year,
        is_donor_logged_in='donor_id' in session,
        is_admin_logged_in='admin_id' in session,
        donor_name=session.get('donor_name', '')
    )

# ----------------- PUBLIC ROUTES ----------------- #

@app.route('/')
def index():
    # Get statistics
    total_events = AnnadanamEvent.query.filter_by(is_verified=True).count()
    serving_now_count = AnnadanamEvent.query.filter_by(is_verified=True, status="Serving Now").count()
    districts_count = db.session.query(db.func.count(db.func.distinct(AnnadanamEvent.district))).filter(AnnadanamEvent.is_verified == True).scalar() or 0
    
    # Recent / Featured Annadanam events
    featured_events = AnnadanamEvent.query.filter_by(is_verified=True).order_by(AnnadanamEvent.is_featured.desc(), AnnadanamEvent.id.desc()).limit(6).all()
    
    # Selected filter day if passed
    selected_day = request.args.get('day', '')
    
    return render_template(
        'index.html',
        total_events=total_events,
        serving_now_count=serving_now_count,
        districts_count=districts_count,
        featured_events=featured_events,
        selected_day=selected_day
    )

@app.route('/events')
def events():
    # Query parameters
    search_query = request.args.get('q', '').strip()
    district = request.args.get('district', '').strip()
    village = request.args.get('village', '').strip()
    day = request.args.get('day', '').strip()
    food_category = request.args.get('category', '').strip()
    status = request.args.get('status', '').strip()
    date_filter = request.args.get('date', '').strip()

    query = AnnadanamEvent.query.filter_by(is_verified=True)

    if search_query:
        search_pattern = f"%{search_query}%"
        query = query.filter(
            db.or_(
                AnnadanamEvent.donor_name.ilike(search_pattern),
                AnnadanamEvent.organization_pandal.ilike(search_pattern),
                AnnadanamEvent.food_details.ilike(search_pattern),
                AnnadanamEvent.village_mandal.ilike(search_pattern),
                AnnadanamEvent.district.ilike(search_pattern),
                AnnadanamEvent.complete_address.ilike(search_pattern)
            )
        )
    
    if district:
        query = query.filter(AnnadanamEvent.district.ilike(f"%{district}%"))
        
    if village:
        query = query.filter(AnnadanamEvent.village_mandal.ilike(f"%{village}%"))

    if day and day != "All":
        query = query.filter(db.or_(AnnadanamEvent.festival_day == day, AnnadanamEvent.festival_day == "All 9 Days"))

    if food_category:
        query = query.filter(AnnadanamEvent.food_category.ilike(f"%{food_category}%"))

    if status:
        query = query.filter(AnnadanamEvent.status == status)

    if date_filter:
        query = query.filter(AnnadanamEvent.event_date == date_filter)

    events_list = query.order_by(
        db.case((AnnadanamEvent.status == 'Serving Now', 1), (AnnadanamEvent.status == 'Available', 2), else_=3),
        AnnadanamEvent.is_featured.desc(),
        AnnadanamEvent.id.desc()
    ).all()

    # Get distinct districts for filter dropdown
    districts = db.session.query(AnnadanamEvent.district).distinct().filter(AnnadanamEvent.is_verified == True).all()
    districts = sorted([d[0] for d in districts if d[0]])

    return render_template(
        'events.html',
        events=events_list,
        districts=districts,
        current_filters={
            'q': search_query,
            'district': district,
            'village': village,
            'day': day,
            'category': food_category,
            'status': status,
            'date': date_filter
        }
    )

@app.route('/event/<int:event_id>')
def event_detail(event_id):
    event = AnnadanamEvent.query.get_or_404(event_id)
    # Increment view count
    event.views_count = (event.views_count or 0) + 1
    db.session.commit()
    
    # Nearby or related events in same district
    related_events = AnnadanamEvent.query.filter(
        AnnadanamEvent.district == event.district,
        AnnadanamEvent.id != event.id,
        AnnadanamEvent.is_verified == True
    ).limit(3).all()

    return render_template('event_detail.html', event=event, related_events=related_events)

@app.route('/api/events')
def api_events():
    """API endpoint returning events for the interactive Leaflet / Map search"""
    district = request.args.get('district', '').strip()
    day = request.args.get('day', '').strip()
    status = request.args.get('status', '').strip()

    query = AnnadanamEvent.query.filter_by(is_verified=True)
    if district:
        query = query.filter(AnnadanamEvent.district.ilike(f"%{district}%"))
    if day and day != "All":
        query = query.filter(db.or_(AnnadanamEvent.festival_day == day, AnnadanamEvent.festival_day == "All 9 Days"))
    if status:
        query = query.filter(AnnadanamEvent.status == status)

    events = query.all()
    return jsonify([e.to_dict() for e in events])

@app.route('/submit-annadanam', methods=['GET', 'POST'])
def submit_annadanam():
    if request.method == 'POST':
        donor_name = request.form.get('donor_name', '').strip()
        mobile_number = request.form.get('mobile_number', '').strip()
        whatsapp_number = request.form.get('whatsapp_number', '').strip() or mobile_number
        organization_pandal = request.form.get('organization_pandal', '').strip()
        
        food_category = request.form.get('food_category', 'Full Meals Prasadam')
        food_details = request.form.get('food_details', '').strip()
        available_quantity = request.form.get('available_quantity', '').strip()
        special_notes = request.form.get('special_notes', '').strip()
        
        festival_day = request.form.get('festival_day', 'Day 1')
        event_date = request.form.get('event_date', str(date.today()))
        distribution_timings = request.form.get('distribution_timings', '').strip()
        
        state = request.form.get('state', 'Telangana')
        district = request.form.get('district', '').strip()
        village_mandal = request.form.get('village_mandal', '').strip()
        complete_address = request.form.get('complete_address', '').strip()
        landmark = request.form.get('landmark', '').strip()
        google_maps_url = request.form.get('google_maps_url', '').strip()
        
        latitude = request.form.get('latitude', type=float)
        longitude = request.form.get('longitude', type=float)

        if not (donor_name and mobile_number and food_details and available_quantity and district and village_mandal and complete_address):
            flash('Please fill in all mandatory fields marked with an asterisk (*).', 'danger')
            return render_template('submit_annadanam.html', form_data=request.form)

        # Check if donor is logged in, link event
        donor_id = session.get('donor_id')
        
        # If google maps link is empty, construct a search link based on address
        if not google_maps_url:
            query_loc = f"{complete_address}, {village_mandal}, {district}".replace(" ", "+")
            google_maps_url = f"https://www.google.com/maps/search/?api=1&query={query_loc}"

        new_event = AnnadanamEvent(
            donor_id=donor_id,
            donor_name=donor_name,
            mobile_number=mobile_number,
            whatsapp_number=whatsapp_number,
            organization_pandal=organization_pandal,
            food_category=food_category,
            food_details=food_details,
            available_quantity=available_quantity,
            special_notes=special_notes,
            festival_day=festival_day,
            event_date=event_date,
            distribution_timings=distribution_timings,
            state=state,
            district=district,
            village_mandal=village_mandal,
            complete_address=complete_address,
            landmark=landmark,
            google_maps_url=google_maps_url,
            latitude=latitude,
            longitude=longitude,
            status='Available',
            is_verified=True # Auto-approved so users immediately see their event
        )
        
        db.session.add(new_event)
        db.session.commit()

        flash('🎉 Jai Ganesha! Your Annadanam event details have been submitted successfully and are now live for devotees to find!', 'success')
        return redirect(url_for('event_detail', event_id=new_event.id))

    return render_template('submit_annadanam.html', form_data={})

@app.route('/about')
def about():
    return render_template('about.html')

# ----------------- DONOR AUTH & DASHBOARD ----------------- #

@app.route('/donor/register', methods=['GET', 'POST'])
def donor_register():
    if request.method == 'POST':
        name = request.form.get('name', '').strip()
        mobile = request.form.get('mobile', '').strip()
        email = request.form.get('email', '').strip()
        organization = request.form.get('organization', '').strip()
        password = request.form.get('password', '')
        confirm_password = request.form.get('confirm_password', '')

        if not name or not mobile or not password:
            flash('Name, Mobile, and Password are required.', 'danger')
            return render_template('donor_register.html')

        if password != confirm_password:
            flash('Passwords do not match.', 'danger')
            return render_template('donor_register.html')

        existing = Donor.query.filter_by(mobile=mobile).first()
        if existing:
            flash('An account with this mobile number already exists. Please log in.', 'warning')
            return redirect(url_for('donor_login'))

        donor = Donor(name=name, mobile=mobile, email=email, organization=organization)
        donor.set_password(password)
        db.session.add(donor)
        db.session.commit()

        session['donor_id'] = donor.id
        session['donor_name'] = donor.name
        session['donor_mobile'] = donor.mobile

        flash('Welcome! Your donor registration is complete. You can now post and manage your Annadanam events.', 'success')
        return redirect(url_for('donor_dashboard'))

    return render_template('donor_register.html')

@app.route('/donor/login', methods=['GET', 'POST'])
def donor_login():
    if request.method == 'POST':
        mobile = request.form.get('mobile', '').strip()
        password = request.form.get('password', '')

        donor = Donor.query.filter_by(mobile=mobile).first()
        if donor and donor.check_password(password):
            session['donor_id'] = donor.id
            session['donor_name'] = donor.name
            session['donor_mobile'] = donor.mobile
            flash(f'Welcome back, {donor.name}!', 'success')
            next_page = request.args.get('next') or url_for('donor_dashboard')
            return redirect(next_page)
        else:
            flash('Invalid mobile number or password.', 'danger')

    return render_template('donor_login.html')

@app.route('/donor/logout')
def donor_logout():
    session.pop('donor_id', None)
    session.pop('donor_name', None)
    session.pop('donor_mobile', None)
    flash('You have been logged out safely.', 'info')
    return redirect(url_for('index'))

@app.route('/donor/dashboard')
@donor_required
def donor_dashboard():
    donor = Donor.query.get(session['donor_id'])
    # Also find events where mobile matches in case they submitted prior to login
    events = AnnadanamEvent.query.filter(
        db.or_(AnnadanamEvent.donor_id == donor.id, AnnadanamEvent.mobile_number == donor.mobile)
    ).order_by(AnnadanamEvent.id.desc()).all()
    
    return render_template('donor_dashboard.html', donor=donor, events=events)

@app.route('/donor/event/<int:event_id>/status', methods=['POST'])
@donor_required
def update_event_status(event_id):
    event = AnnadanamEvent.query.get_or_404(event_id)
    # Check ownership
    if event.donor_id != session['donor_id'] and event.mobile_number != session.get('donor_mobile'):
        flash('Unauthorized to edit this event.', 'danger')
        return redirect(url_for('donor_dashboard'))

    new_status = request.form.get('status')
    if new_status in ['Available', 'Serving Now', 'Exhausted', 'Completed']:
        event.status = new_status
        db.session.commit()
        flash(f'Status updated to "{new_status}" successfully!', 'success')
    return redirect(url_for('donor_dashboard'))

# ----------------- ADMIN PORTAL ----------------- #

@app.route('/admin/login', methods=['GET', 'POST'])
def admin_login():
    if request.method == 'POST':
        username = request.form.get('username', '').strip()
        password = request.form.get('password', '')

        admin = AdminUser.query.filter_by(username=username).first()
        if admin and admin.check_password(password):
            session['admin_id'] = admin.id
            session['admin_username'] = admin.username
            flash('Admin authentication successful.', 'success')
            next_page = request.args.get('next') or url_for('admin_dashboard')
            return redirect(next_page)
        else:
            flash('Invalid admin credentials.', 'danger')

    return render_template('admin/login.html')

@app.route('/admin/logout')
def admin_logout():
    session.pop('admin_id', None)
    session.pop('admin_username', None)
    flash('Logged out from admin dashboard.', 'info')
    return redirect(url_for('admin_login'))

@app.route('/admin/dashboard')
@admin_required
def admin_dashboard():
    total_events = AnnadanamEvent.query.count()
    verified_events = AnnadanamEvent.query.filter_by(is_verified=True).count()
    pending_events = AnnadanamEvent.query.filter_by(is_verified=False).count()
    total_donors = Donor.query.count()

    all_events = AnnadanamEvent.query.order_by(AnnadanamEvent.id.desc()).all()

    return render_template(
        'admin/dashboard.html',
        total_events=total_events,
        verified_events=verified_events,
        pending_events=pending_events,
        total_donors=total_donors,
        events=all_events
    )

@app.route('/admin/event/<int:event_id>/verify', methods=['POST'])
@admin_required
def admin_toggle_verify(event_id):
    event = AnnadanamEvent.query.get_or_404(event_id)
    event.is_verified = not event.is_verified
    db.session.commit()
    status_str = "Verified / Active" if event.is_verified else "Unverified / Hidden"
    flash(f'Event #{event.id} marked as {status_str}.', 'success')
    return redirect(url_for('admin_dashboard'))

@app.route('/admin/event/<int:event_id>/feature', methods=['POST'])
@admin_required
def admin_toggle_feature(event_id):
    event = AnnadanamEvent.query.get_or_404(event_id)
    event.is_featured = not event.is_featured
    db.session.commit()
    feat_str = "Featured on Home" if event.is_featured else "Removed from Featured"
    flash(f'Event #{event.id} {feat_str}.', 'success')
    return redirect(url_for('admin_dashboard'))

@app.route('/admin/event/<int:event_id>/delete', methods=['POST'])
@admin_required
def admin_delete_event(event_id):
    event = AnnadanamEvent.query.get_or_404(event_id)
    db.session.delete(event)
    db.session.commit()
    flash(f'Event #{event_id} deleted successfully.', 'info')
    return redirect(url_for('admin_dashboard'))

def init_db():
    with app.app_context():
        db.create_all()
        # Create default admin if not existing
        admin = AdminUser.query.filter_by(username=app.config['ADMIN_DEFAULT_USERNAME']).first()
        if not admin:
            admin = AdminUser(username=app.config['ADMIN_DEFAULT_USERNAME'])
            admin.set_password(app.config['ADMIN_DEFAULT_PASSWORD'])
            db.session.add(admin)
            db.session.commit()
            print(f"Default admin created: {app.config['ADMIN_DEFAULT_USERNAME']}")

if __name__ == '__main__':
    init_db()
    app.run(debug=True, host='0.0.0.0', port=5000)
