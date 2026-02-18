import pytest
import sqlite3
import requests
import json
import hashlib
from datetime import datetime
import os

# Base URL
BASE_URL = "http://localhost:5000"

class TestDatabase:
    """Database Testing"""
    
    def test_database_exists(self):
        """Test if database file exists"""
        assert os.path.exists('railway.db'), "Database file not found"
    
    def test_database_tables(self):
        """Test if all required tables exist"""
        conn = sqlite3.connect('railway.db')
        cursor = conn.cursor()
        cursor.execute("SELECT name FROM sqlite_master WHERE type='table'")
        tables = [row[0] for row in cursor.fetchall()]
        conn.close()
        
        required_tables = [
            'admin', 'crowd_updates', 'emergency_alerts',
            'women_safety_alerts', 'ticket_bookings', 'destination_alerts'
        ]
        
        for table in required_tables:
            assert table in tables, f"Table {table} not found"
    
    def test_admin_user_exists(self):
        """Test if default admin exists"""
        conn = sqlite3.connect('railway.db')
        cursor = conn.cursor()
        cursor.execute("SELECT COUNT(*) FROM admin WHERE username = 'admin'")
        count = cursor.fetchone()[0]
        conn.close()
        
        assert count > 0, "Default admin user not found"
    
    def test_password_hashed(self):
        """Test if password is hashed"""
        conn = sqlite3.connect('railway.db')
        cursor = conn.cursor()
        cursor.execute("SELECT password FROM admin WHERE username = 'admin'")
        password = cursor.fetchone()[0]
        conn.close()
        
        # Check if password is hashed (should be 64 characters for SHA256)
        assert len(password) == 64, "Password is not properly hashed"

class TestWebPages:
    """Web Page Accessibility Testing"""
    
    def test_home_page(self):
        """Test home page loads"""
        response = requests.get(f"{BASE_URL}/")
        assert response.status_code == 200, "Home page not accessible"
    
    def test_admin_login_page(self):
        """Test admin login page loads"""
        response = requests.get(f"{BASE_URL}/admin/login")
        assert response.status_code == 200, "Admin login page not accessible"
    
    def test_passenger_view_page(self):
        """Test passenger view page loads"""
        response = requests.get(f"{BASE_URL}/passenger/view")
        assert response.status_code == 200, "Passenger view page not accessible"
    
    def test_train_schedule_page(self):
        """Test train schedule page loads"""
        response = requests.get(f"{BASE_URL}/train-schedule")
        assert response.status_code == 200, "Train schedule page not accessible"
    
    def test_emergency_alert_page(self):
        """Test emergency alert page loads"""
        response = requests.get(f"{BASE_URL}/passenger/emergency")
        assert response.status_code == 200, "Emergency alert page not accessible"
    
    def test_ticket_booking_page(self):
        """Test ticket booking page loads"""
        response = requests.get(f"{BASE_URL}/passenger/ticket-booking")
        assert response.status_code == 200, "Ticket booking page not accessible"

class TestAPI:
    """API Endpoint Testing"""
    
    def test_api_stations(self):
        """Test stations API"""
        response = requests.get(f"{BASE_URL}/api/stations")
        assert response.status_code == 200, "Stations API failed"
        data = response.json()
        assert len(data) > 0, "No stations returned"
        assert 'Chennai Central' in data, "Chennai Central not in stations"
    
    def test_api_trains(self):
        """Test trains API"""
        response = requests.get(f"{BASE_URL}/api/trains")
        assert response.status_code == 200, "Trains API failed"
        data = response.json()
        assert len(data) == 12, "Expected 12 trains"
    
    def test_api_train_availability(self):
        """Test train availability API"""
        response = requests.get(f"{BASE_URL}/api/train-availability")
        assert response.status_code == 200, "Train availability API failed"
        data = response.json()
        assert len(data) > 0, "No availability data"
        
        # Check data structure
        first_train = data[0]
        required_fields = ['number', 'name', 'total_seats', 'available', 'booked']
        for field in required_fields:
            assert field in first_train, f"Field {field} missing in availability data"
    
    def test_api_platforms(self):
        """Test platforms API"""
        response = requests.get(f"{BASE_URL}/api/platforms/Chennai Central")
        assert response.status_code == 200, "Platforms API failed"
        data = response.json()
        assert len(data) == 10, "Chennai Central should have 10 platforms"

class TestAdminFunctionality:
    """Admin Functionality Testing"""
    
    @pytest.fixture
    def admin_session(self):
        """Create admin session"""
        session = requests.Session()
        # Login
        login_data = {
            'username': 'admin',
            'password': 'admin123'
        }
        response = session.post(f"{BASE_URL}/admin/login", data=login_data)
        return session
    
    def test_admin_login_valid(self, admin_session):
        """Test valid admin login"""
        response = admin_session.get(f"{BASE_URL}/admin/dashboard")
        assert response.status_code == 200, "Admin dashboard not accessible after login"
    
    def test_admin_dashboard_access(self, admin_session):
        """Test admin can access dashboard"""
        response = admin_session.get(f"{BASE_URL}/admin/dashboard")
        assert response.status_code == 200, "Cannot access admin dashboard"
        assert b'Dashboard' in response.content, "Dashboard content not found"
    
    def test_crowd_update_page_access(self, admin_session):
        """Test admin can access crowd update page"""
        response = admin_session.get(f"{BASE_URL}/admin/crowd-update")
        assert response.status_code == 200, "Cannot access crowd update page"
    
    def test_alerts_page_access(self, admin_session):
        """Test admin can access alerts page"""
        response = admin_session.get(f"{BASE_URL}/admin/alerts")
        assert response.status_code == 200, "Cannot access alerts page"
    
    def test_blockchain_page_access(self, admin_session):
        """Test admin can access blockchain page"""
        response = admin_session.get(f"{BASE_URL}/admin/blockchain")
        assert response.status_code == 200, "Cannot access blockchain page"
    
    def test_reports_page_access(self, admin_session):
        """Test admin can access reports page"""
        response = admin_session.get(f"{BASE_URL}/admin/reports")
        assert response.status_code == 200, "Cannot access reports page"

class TestDataIntegrity:
    """Data Integrity Testing"""
    
    def test_crowd_data_persistence(self):
        """Test crowd data is stored correctly"""
        conn = sqlite3.connect('railway.db')
        cursor = conn.cursor()
        
        # Get count before
        cursor.execute("SELECT COUNT(*) FROM crowd_updates")
        count_before = cursor.fetchone()[0]
        
        # Insert test data
        test_data = (
            'Test Station', 'Low', '1', 'Test Train', 'Test Remark', 
            'admin', 'test_hash_' + str(datetime.now().timestamp())
        )
        cursor.execute('''
            INSERT INTO crowd_updates 
            (station_name, crowd_level, platform_no, train_name, remarks, updated_by, blockchain_hash)
            VALUES (?, ?, ?, ?, ?, ?, ?)
        ''', test_data)
        conn.commit()
        
        # Get count after
        cursor.execute("SELECT COUNT(*) FROM crowd_updates")
        count_after = cursor.fetchone()[0]
        
        # Cleanup
        cursor.execute("DELETE FROM crowd_updates WHERE station_name = 'Test Station'")
        conn.commit()
        conn.close()
        
        assert count_after == count_before + 1, "Crowd data not persisted correctly"
    
   

class TestBlockchain:
    """Blockchain Testing"""
    
    def test_blockchain_initialization(self):
        """Test blockchain is initialized"""
        from blockchain import railway_blockchain
        assert len(railway_blockchain.chain) > 0, "Blockchain not initialized"
        assert railway_blockchain.chain[0].index == 0, "Genesis block missing"
    
    def test_blockchain_validity(self):
        """Test blockchain integrity"""
        from blockchain import railway_blockchain
        assert railway_blockchain.is_chain_valid(), "Blockchain is invalid"
    
    def test_block_hashing(self):
        """Test block hash generation"""
        from blockchain import railway_blockchain
        
        # Add a test block
        test_data = {'type': 'test', 'data': 'test_block'}
        block_hash = railway_blockchain.add_block(test_data)
        
        assert block_hash is not None, "Block hash not generated"
        assert len(block_hash) == 64, "Block hash should be 64 characters (SHA256)"

class TestSecurity:
    """Security Testing"""
    
    def test_unauthorized_admin_access(self):
        """Test unauthorized access to admin pages is blocked"""
        response = requests.get(f"{BASE_URL}/admin/dashboard")
        # Should redirect to login
        assert response.url.endswith('/admin/login') or response.status_code == 302, \
            "Unauthorized access not blocked"
    
    def test_session_management(self):
        """Test session management"""
        session = requests.Session()
        
        # Try to access admin page without login
        response = session.get(f"{BASE_URL}/admin/dashboard")
        assert '/admin/login' in response.url, "Session not managed properly"
    
    def test_password_encryption(self):
        """Test passwords are encrypted"""
        test_password = "admin123"
        expected_hash = hashlib.sha256(test_password.encode()).hexdigest()
        
        conn = sqlite3.connect('railway.db')
        cursor = conn.cursor()
        cursor.execute("SELECT password FROM admin WHERE username = 'admin'")
        stored_hash = cursor.fetchone()[0]
        conn.close()
        
        assert stored_hash == expected_hash, "Password not properly encrypted"

class TestPerformance:
    """Performance Testing"""
    
    def test_page_load_time(self):
        """Test page loads within acceptable time"""
        import time
        
        start = time.time()
        response = requests.get(f"{BASE_URL}/")
        end = time.time()
        
        load_time = end - start
        assert load_time < 3, f"Page load time too slow: {load_time}s"
    
   

class TestEmailConfiguration:
    """Email Configuration Testing"""
    
    def test_email_config_exists(self):
        """Test email configuration is set"""
        # Read app.py to check email config
        with open('app.py', 'r') as f:
            content = f.read()
            assert 'MAIL_SERVER' in content, "Email server not configured"
            assert 'MAIL_USERNAME' in content, "Email username not configured"
            assert 'MAIL_PASSWORD' in content, "Email password not configured"

# Test Report Generator
def generate_test_report(results_file='test_results.html'):
    """Generate HTML test report"""
    import subprocess
    
    # Run pytest with HTML report
    cmd = [
        'pytest',
        'test_railway_system.py',
        '-v',
        '--html=' + results_file,
        '--self-contained-html'
    ]
    
    subprocess.run(cmd)
    print(f"\n✅ Test report generated: {results_file}")

if __name__ == '__main__':
    print("🧪 Starting Smart Railway System Tests...")
    print("=" * 60)
    
    # Run tests with detailed output
    pytest.main([
        __file__,
        '-v',
        '--html=test_report.html',
        '--self-contained-html',
        '--tb=short'
    ])
    
    print("\n" + "=" * 60)
    print("✅ Testing completed!")
    print("📊 Check test_report.html for detailed results")
    