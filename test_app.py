"""Verification test for Vinayaka Chavithi Annadanam Finder"""
import sys
import io
# Set stdout to utf-8 safe
if sys.platform == 'win32':
    sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')

from app import app, db
from models import AnnadanamEvent, Donor, AdminUser

def run_tests():
    client = app.test_client()
    print("Testing public routes...")
    
    # 1. Test Home Page
    res = client.get('/')
    assert res.status_code == 200, f"Home failed with status {res.status_code}"
    assert b"Vinayaka Chavithi" in res.data
    assert b"Annadanam" in res.data
    print("✓ Home page loaded successfully")

    # 2. Test Events Directory
    res = client.get('/events')
    assert res.status_code == 200
    assert b"Directory" in res.data
    print("✓ Events directory loaded successfully")

    # 3. Test Filter by District
    res = client.get('/events?district=Hyderabad')
    assert res.status_code == 200
    assert b"Hyderabad" in res.data
    print("✓ Filter by district works")

    # 4. Test Event Detail
    res = client.get('/event/1')
    assert res.status_code == 200
    assert b"Mahaprasadam" in res.data or b"Google Maps" in res.data
    print("✓ Event detail page loaded successfully")

    # 5. Test API endpoint for Leaflet Map
    res = client.get('/api/events')
    assert res.status_code == 200
    data = res.get_json()
    assert isinstance(data, list) and len(data) > 0
    print(f"✓ Map API returned {len(data)} geo-located events")

    # 6. Test About page
    res = client.get('/about')
    assert res.status_code == 200
    print("✓ About page loaded successfully")

    # 7. Test Admin Login & Dashboard
    with client.session_transaction() as sess:
        sess['admin_id'] = 1
        sess['admin_username'] = 'admin'
    res = client.get('/admin/dashboard')
    assert res.status_code == 200
    assert b"Admin Moderation" in res.data
    print("✓ Admin dashboard loaded successfully")

    # 8. Test Submit Form GET
    res = client.get('/submit-annadanam')
    assert res.status_code == 200
    assert b"Post Your Annadanam" in res.data
    print("✓ Submit Annadanam form loaded successfully")

    print("\n🎉 ALL APPLICATION TESTS PASSED SUCCESSFULLY!")

if __name__ == '__main__':
    run_tests()
