"""
Seed script to populate realistic Vinayaka Chavithi Annadanam events
covering 9 days of celebrations across various districts.
"""
from app import app, db, init_db
from models import Donor, AnnadanamEvent, AdminUser
from datetime import date, timedelta

def seed_database():
    with app.app_context():
        init_db()
        
        # Check if already seeded
        if AnnadanamEvent.query.count() > 0:
            print("Database already contains events. Skipping seed.")
            return

        print("Seeding Vinayaka Chavithi Annadanam events...")

        # Create demo donors
        donors_data = [
            {
                "name": "K. Venkata Rao & Family",
                "mobile": "9848022334",
                "email": "venkatarao@gmail.com",
                "org": "Khairatabad Devotees Welfare Trust"
            },
            {
                "name": "S. Rajesh Kumar",
                "mobile": "9440112233",
                "email": "rajesh.k@gmail.com",
                "org": "Balapur Ganesh Utsava Samithi"
            },
            {
                "name": "M. Srinivasulu Reddy",
                "mobile": "9988776655",
                "email": "srinivasulu@reddyfoods.org",
                "org": "Sri Vinayaka Seva Samstha"
            },
            {
                "name": "G. Lakshmi Narayana",
                "mobile": "9123456780",
                "email": "narayana.g@vizagdevotees.com",
                "org": "Visakha Youth Cultural Association"
            },
            {
                "name": "P. Ramachandra Murthy",
                "mobile": "9866554433",
                "email": "murthy.ram@vijayawada.org",
                "org": "Krishna District Annadanam Trust"
            }
        ]

        created_donors = []
        for d in donors_data:
            donor = Donor(
                name=d["name"],
                mobile=d["mobile"],
                email=d["email"],
                organization=d["org"]
            )
            donor.set_password("donor123")
            db.session.add(donor)
            created_donors.append(donor)
        
        db.session.commit()

        base_date = date.today()

        sample_events = [
            {
                "donor_id": created_donors[0].id,
                "donor_name": "K. Venkata Rao",
                "mobile_number": "9848022334",
                "whatsapp_number": "9848022334",
                "organization_pandal": "Khairatabad Bada Ganesh Mandapam Devotees Samithi",
                "food_category": "Full Meals Prasadam",
                "food_details": "Temple Sambar Rice, Tamarind Pulihara, Daddojanam (Curd Rice), Bellam Pongali, Laddu, Buttermilk",
                "available_quantity": "5000+ Devotees daily",
                "special_notes": "Continuous distribution counter, separate lines for senior citizens & women, clean drinking water",
                "festival_day": "All 9 Days",
                "event_date": str(base_date),
                "distribution_timings": "11:30 AM to 4:00 PM & 7:00 PM to 10:00 PM",
                "state": "Telangana",
                "district": "Hyderabad",
                "village_mandal": "Khairatabad",
                "complete_address": "Adjacent to Khairatabad Railway Station, Bada Ganesh Pandal Grounds",
                "landmark": "Near Khairatabad Metro Station",
                "google_maps_url": "https://maps.google.com/?q=17.4116,78.4611",
                "latitude": 17.4116,
                "longitude": 78.4611,
                "status": "Serving Now",
                "is_featured": True
            },
            {
                "donor_id": created_donors[1].id,
                "donor_name": "S. Rajesh Kumar",
                "mobile_number": "9440112233",
                "whatsapp_number": "9440112233",
                "organization_pandal": "Balapur Ganesh Utsava Samithi & Village Elders",
                "food_category": "Full Meals Prasadam",
                "food_details": "Authentic Bagara Rice, Kathirikai/Mirchi Ka Salan, Dalcha, Sweet Boondi, Banana",
                "available_quantity": "3000 Devotees",
                "special_notes": "Dining hall arranged under shamiana with eco-friendly leaf plates",
                "festival_day": "Day 1",
                "event_date": str(base_date),
                "distribution_timings": "12:30 PM to 4:00 PM",
                "state": "Telangana",
                "district": "Hyderabad",
                "village_mandal": "Balapur",
                "complete_address": "Balapur Old Village Chowrasta, Temple Grounds",
                "landmark": "Near Historic Balapur Kadiyam Pandal",
                "google_maps_url": "https://maps.google.com/?q=17.3228,78.5146",
                "latitude": 17.3228,
                "longitude": 78.5146,
                "status": "Available",
                "is_featured": True
            },
            {
                "donor_id": created_donors[2].id,
                "donor_name": "M. Srinivasulu Reddy",
                "mobile_number": "9988776655",
                "whatsapp_number": "9988776655",
                "organization_pandal": "Dilsukhnagar Merchants Association & Sai Vinayaka Pandal",
                "food_category": "Pulihara & Pongali",
                "food_details": "Andhra Style Chinthapandu Pulihara, Hot Ghee Pongal, Kesari Sweet, Fresh Masala Buttermilk",
                "available_quantity": "1500 Food Packets",
                "special_notes": "Hygienically pre-packed disposable containers for easy take-away",
                "festival_day": "Day 2",
                "event_date": str(base_date + timedelta(days=1)),
                "distribution_timings": "12:00 PM to 3:00 PM",
                "state": "Telangana",
                "district": "Hyderabad",
                "village_mandal": "Dilsukhnagar",
                "complete_address": "Shop No 14, Main Road, Beside Rajdhani Theatre",
                "landmark": "Near Dilsukhnagar Bus Depot",
                "google_maps_url": "https://maps.google.com/?q=17.3688,78.5247",
                "latitude": 17.3688,
                "longitude": 78.5247,
                "status": "Available",
                "is_featured": False
            },
            {
                "donor_id": created_donors[3].id,
                "donor_name": "G. Lakshmi Narayana",
                "mobile_number": "9123456780",
                "whatsapp_number": "9123456780",
                "organization_pandal": "Visakha Youth Cultural Association (MVP Colony)",
                "food_category": "Full Meals Prasadam",
                "food_details": "Pulao Rice, Tomato Pappu, Gongura Chutney, Ghee Sambar, Curd, Semiaya Payasam",
                "available_quantity": "2000 Meals",
                "special_notes": "Sitting dining arrangement with safe drinking water station",
                "festival_day": "Day 3",
                "event_date": str(base_date + timedelta(days=2)),
                "distribution_timings": "12:30 PM to 3:30 PM",
                "state": "Andhra Pradesh",
                "district": "Visakhapatnam",
                "village_mandal": "MVP Colony",
                "complete_address": "Sector 3 Playground, MVP Colony Main Road",
                "landmark": "Opposite AS Raja Ground",
                "google_maps_url": "https://maps.google.com/?q=17.7412,83.3341",
                "latitude": 17.7412,
                "longitude": 83.3341,
                "status": "Available",
                "is_featured": True
            },
            {
                "donor_id": created_donors[4].id,
                "donor_name": "P. Ramachandra Murthy",
                "mobile_number": "9866554433",
                "whatsapp_number": "9866554433",
                "organization_pandal": "Sri Durga Vinayaka Bhakta Mandali, Benz Circle",
                "food_category": "Full Meals Prasadam",
                "food_details": "Steamed Sona Masoori Rice, Mango Dal, Drumstick Sambar, Majjiga Pulusu, Bellam Paramannam, Kaju Laddu",
                "available_quantity": "2500 Devotees",
                "special_notes": "All are invited, prasadam served in traditional eco plantain banana leaves",
                "festival_day": "Day 4",
                "event_date": str(base_date + timedelta(days=3)),
                "distribution_timings": "12:00 PM to 4:00 PM & 8:00 PM to 10:00 PM",
                "state": "Andhra Pradesh",
                "district": "Vijayawada (NTR)",
                "village_mandal": "Benz Circle",
                "complete_address": "Near Jyothi Convention Hall, Bandar Road",
                "landmark": "Behind Trendset Mall",
                "google_maps_url": "https://maps.google.com/?q=16.4988,80.6548",
                "latitude": 16.4988,
                "longitude": 80.6548,
                "status": "Available",
                "is_featured": True
            },
            {
                "donor_id": None,
                "donor_name": "K. Thirupathi Swamy",
                "mobile_number": "9701234567",
                "whatsapp_number": "9701234567",
                "organization_pandal": "Ekashila Ganesh Youth Club, Hanamkonda",
                "food_category": "Full Meals Prasadam",
                "food_details": "Bagara Rice, Dal Tadka, Aloo Kurma, Lemon Rice, Rava Kesari",
                "available_quantity": "1200 Meals",
                "special_notes": "Free distribution to all passersby, students, and workers",
                "festival_day": "Day 5",
                "event_date": str(base_date + timedelta(days=4)),
                "distribution_timings": "1:00 PM to 4:00 PM",
                "state": "Telangana",
                "district": "Warangal",
                "village_mandal": "Hanamkonda",
                "complete_address": "Nakkalagutta Main Road, Near Public Gardens",
                "landmark": "Near Kakatiya University Cross Roads",
                "google_maps_url": "https://maps.google.com/?q=17.9942,79.5546",
                "latitude": 17.9942,
                "longitude": 79.5546,
                "status": "Available",
                "is_featured": False
            },
            {
                "donor_id": None,
                "donor_name": "Anjaneyulu & Friends",
                "mobile_number": "9849988771",
                "whatsapp_number": "9849988771",
                "organization_pandal": "Siddhi Vinayaka Seva Trust, Brodipet",
                "food_category": "Tiffin & Sweets",
                "food_details": "Steamed Idli with Sambar & Chutney, Lemon Pulihora, Ravva Halwa, Warm Mysore Pak",
                "available_quantity": "800 Packs",
                "special_notes": "Morning prasadam distribution starts right after Maha Harathi",
                "festival_day": "Day 6",
                "event_date": str(base_date + timedelta(days=5)),
                "distribution_timings": "8:30 AM to 11:30 AM",
                "state": "Andhra Pradesh",
                "district": "Guntur",
                "village_mandal": "Brodipet",
                "complete_address": "4/1 Brodipet, Near Guntur Railway Station Road",
                "landmark": "Near Venkateswara Swamy Temple",
                "google_maps_url": "https://maps.google.com/?q=16.3067,80.4365",
                "latitude": 16.3067,
                "longitude": 80.4365,
                "status": "Available",
                "is_featured": False
            },
            {
                "donor_id": None,
                "donor_name": "Tirupati Youth Federation",
                "mobile_number": "9949112244",
                "whatsapp_number": "9949112244",
                "organization_pandal": "Govinda Vinayaka Pandal, Alipiri",
                "food_category": "Full Meals Prasadam",
                "food_details": "Tirumala style Chitrannam, Ghee Pongal, Sambar Rice, Curd Rice, Boondi Laddu",
                "available_quantity": "4000 Devotees",
                "special_notes": "Annadanam for pilgrims and local devotees",
                "festival_day": "Day 9",
                "event_date": str(base_date + timedelta(days=8)),
                "distribution_timings": "11:00 AM to 5:00 PM (Grand Maha Annadanam)",
                "state": "Andhra Pradesh",
                "district": "Tirupati",
                "village_mandal": "Alipiri Bypass",
                "complete_address": "Alipiri Link Road, Foothills Ground",
                "landmark": "Near Garuda Circle",
                "google_maps_url": "https://maps.google.com/?q=13.6515,79.4002",
                "latitude": 13.6515,
                "longitude": 79.4002,
                "status": "Available",
                "is_featured": True
            }
        ]

        for ev in sample_events:
            event = AnnadanamEvent(**ev, is_verified=True)
            db.session.add(event)

        db.session.commit()
        print(f"Successfully seeded {len(sample_events)} Annadanam events and {len(donors_data)} donors!")

if __name__ == '__main__':
    seed_database()
