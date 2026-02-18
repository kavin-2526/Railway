from flask import Flask, render_template, request, redirect, url_for, session, flash, jsonify
from flask_mail import Mail, Message
import sqlite3
import hashlib
from datetime import datetime, timedelta
import random
import string
from blockchain import railway_blockchain

app = Flask(__name__)
app.secret_key = 'railway_secret_key_2025'

# Email Configuration
app.config['MAIL_SERVER'] = 'smtp.gmail.com'
app.config['MAIL_PORT'] = 587
app.config['MAIL_USE_TLS'] = True
app.config['MAIL_USERNAME'] = 'eslineslin333@gmail.com'
app.config['MAIL_PASSWORD'] = 'hzpl fuqt zlwp haus'
app.config['MAIL_DEFAULT_SENDER'] = 'eslineslin333@gmail.com'
mail = Mail(app)

# Tamil Nadu Railway Data
STATIONS = [
    'Chennai Central', 'Chennai Egmore', 'Tambaram', 'Coimbatore Junction',
    'Madurai Junction', 'Trichy Junction', 'Salem Junction', 'Erode Junction',
    'Tiruppur', 'Villupuram Junction', 'Thanjavur', 'Kumbakonam',
    'Dindigul Junction', 'Karur', 'Kanchipuram', 'Chengalpattu',
    'Katpadi Junction', 'Arakkonam', 'Nagercoil Junction', 'Rameswaram',
    'Tuticorin', 'Kanyakumari'
]

PLATFORMS = {
    'Chennai Central': ['1', '2', '3', '4', '5', '6', '7', '8', '9', '10'],
    'Chennai Egmore': ['1', '2', '3', '4', '5', '6'],
    'Coimbatore Junction': ['1', '2', '3', '4', '5', '6'],
    'Madurai Junction': ['1', '2', '3', '4', '5'],
    'Trichy Junction': ['1', '2', '3', '4'],
    'Salem Junction': ['1', '2', '3', '4'],
    'Tambaram': ['1', '2', '3'],
    'Erode Junction': ['1', '2', '3', '4'],
    'Tiruppur': ['1', '2'],
    'Villupuram Junction': ['1', '2', '3', '4'],
    'Thanjavur': ['1', '2'],
    'Kumbakonam': ['1', '2'],
    'Dindigul Junction': ['1', '2', '3'],
    'Karur': ['1', '2'],
    'Kanchipuram': ['1'],
    'Chengalpattu': ['1', '2', '3'],
    'Katpadi Junction': ['1', '2', '3', '4'],
    'Arakkonam': ['1', '2', '3'],
    'Nagercoil Junction': ['1', '2'],
    'Rameswaram': ['1'],
    'Tuticorin': ['1', '2'],
    'Kanyakumari': ['1']
}

TRAINS = [
    {
        'number': '12617', 
        'name': 'Pandian Express', 
        'route': 'Chennai Egmore - Madurai', 
        'seats': 450,
        'departure_time': '21:00',
        'arrival_time': '05:30',
        'departure_station': 'Chennai Egmore',
        'arrival_station': 'Madurai Junction',
        'duration': '8h 30m',
        'frequency': 'Daily',
        'class_available': 'SL, 3A, 2A, 1A',
        'schedule': [
            {'station': 'Chennai Egmore', 'arrival': '--', 'departure': '21:00', 'platform': '3'},
            {'station': 'Tambaram', 'arrival': '21:25', 'departure': '21:27', 'platform': '2'},
            {'station': 'Chengalpattu', 'arrival': '22:00', 'departure': '22:02', 'platform': '1'},
            {'station': 'Villupuram Junction', 'arrival': '23:35', 'departure': '23:40', 'platform': '3'},
            {'station': 'Trichy Junction', 'arrival': '02:15', 'departure': '02:20', 'platform': '4'},
            {'station': 'Dindigul Junction', 'arrival': '04:30', 'departure': '04:32', 'platform': '2'},
            {'station': 'Madurai Junction', 'arrival': '05:30', 'departure': '--', 'platform': '5'}
        ]
    },
    {
        'number': '12635', 
        'name': 'Vaigai Express', 
        'route': 'Chennai Egmore - Madurai', 
        'seats': 380,
        'departure_time': '13:40',
        'arrival_time': '21:25',
        'departure_station': 'Chennai Egmore',
        'arrival_station': 'Madurai Junction',
        'duration': '7h 45m',
        'frequency': 'Daily',
        'class_available': '2S, CC, SL, 3A',
        'schedule': [
            {'station': 'Chennai Egmore', 'arrival': '--', 'departure': '13:40', 'platform': '5'},
            {'station': 'Tambaram', 'arrival': '14:10', 'departure': '14:12', 'platform': '1'},
            {'station': 'Chengalpattu', 'arrival': '14:45', 'departure': '14:47', 'platform': '2'},
            {'station': 'Villupuram Junction', 'arrival': '16:15', 'departure': '16:20', 'platform': '4'},
            {'station': 'Trichy Junction', 'arrival': '19:00', 'departure': '19:05', 'platform': '3'},
            {'station': 'Dindigul Junction', 'arrival': '20:45', 'departure': '20:47', 'platform': '1'},
            {'station': 'Madurai Junction', 'arrival': '21:25', 'departure': '--', 'platform': '2'}
        ]
    },
    {
        'number': '12676', 
        'name': 'Kovai Express', 
        'route': 'Chennai Central - Coimbatore', 
        'seats': 420,
        'departure_time': '06:20',
        'arrival_time': '13:30',
        'departure_station': 'Chennai Central',
        'arrival_station': 'Coimbatore Junction',
        'duration': '7h 10m',
        'frequency': 'Daily',
        'class_available': 'SL, 3A, 2A',
        'schedule': [
            {'station': 'Chennai Central', 'arrival': '--', 'departure': '06:20', 'platform': '7'},
            {'station': 'Arakkonam', 'arrival': '07:28', 'departure': '07:30', 'platform': '2'},
            {'station': 'Katpadi Junction', 'arrival': '08:05', 'departure': '08:10', 'platform': '3'},
            {'station': 'Salem Junction', 'arrival': '10:15', 'departure': '10:20', 'platform': '4'},
            {'station': 'Erode Junction', 'arrival': '11:30', 'departure': '11:35', 'platform': '2'},
            {'station': 'Tiruppur', 'arrival': '12:10', 'departure': '12:12', 'platform': '1'},
            {'station': 'Coimbatore Junction', 'arrival': '13:30', 'departure': '--', 'platform': '5'}
        ]
    },
    {
        'number': '12671', 
        'name': 'Nilgiri Express', 
        'route': 'Chennai Central - Mettupalayam', 
        'seats': 400,
        'departure_time': '21:00',
        'arrival_time': '06:25',
        'departure_station': 'Chennai Central',
        'arrival_station': 'Mettupalayam',
        'duration': '9h 25m',
        'frequency': 'Daily',
        'class_available': 'SL, 3A, 2A, 1A',
        'schedule': [
            {'station': 'Chennai Central', 'arrival': '--', 'departure': '21:00', 'platform': '9'},
            {'station': 'Katpadi Junction', 'arrival': '22:48', 'departure': '22:50', 'platform': '4'},
            {'station': 'Salem Junction', 'arrival': '01:15', 'departure': '01:20', 'platform': '3'},
            {'station': 'Erode Junction', 'arrival': '02:40', 'departure': '02:45', 'platform': '3'},
            {'station': 'Tiruppur', 'arrival': '03:23', 'departure': '03:25', 'platform': '2'},
            {'station': 'Coimbatore Junction', 'arrival': '04:45', 'departure': '04:50', 'platform': '4'},
            {'station': 'Mettupalayam', 'arrival': '06:25', 'departure': '--', 'platform': '1'}
        ]
    },
    {
        'number': '12639', 
        'name': 'Brindavan Express', 
        'route': 'Chennai Central - Bangalore', 
        'seats': 500,
        'departure_time': '07:30',
        'arrival_time': '13:15',
        'departure_station': 'Chennai Central',
        'arrival_station': 'Bangalore City',
        'duration': '5h 45m',
        'frequency': 'Daily',
        'class_available': 'CC, 2S, SL',
        'schedule': [
            {'station': 'Chennai Central', 'arrival': '--', 'departure': '07:30', 'platform': '10'},
            {'station': 'Arakkonam', 'arrival': '08:33', 'departure': '08:35', 'platform': '1'},
            {'station': 'Katpadi Junction', 'arrival': '09:08', 'departure': '09:10', 'platform': '2'},
            {'station': 'Jolarpettai', 'arrival': '10:28', 'departure': '10:30', 'platform': '4'},
            {'station': 'Bangalore City', 'arrival': '13:15', 'departure': '--', 'platform': '8'}
        ]
    },
    {
        'number': '12028', 
        'name': 'Shatabdi Express', 
        'route': 'Chennai Central - Coimbatore', 
        'seats': 350,
        'departure_time': '06:00',
        'arrival_time': '12:05',
        'departure_station': 'Chennai Central',
        'arrival_station': 'Coimbatore Junction',
        'duration': '6h 05m',
        'frequency': 'Daily except Tuesday',
        'class_available': 'CC, EC',
        'schedule': [
            {'station': 'Chennai Central', 'arrival': '--', 'departure': '06:00', 'platform': '8'},
            {'station': 'Katpadi Junction', 'arrival': '07:48', 'departure': '07:50', 'platform': '3'},
            {'station': 'Salem Junction', 'arrival': '09:40', 'departure': '09:45', 'platform': '2'},
            {'station': 'Erode Junction', 'arrival': '10:58', 'departure': '11:00', 'platform': '4'},
            {'station': 'Tiruppur', 'arrival': '11:33', 'departure': '11:35', 'platform': '1'},
            {'station': 'Coimbatore Junction', 'arrival': '12:05', 'departure': '--', 'platform': '6'}
        ]
    },
    {
        'number': '12163', 
        'name': 'Chennai Mail', 
        'route': 'Chennai - Mumbai', 
        'seats': 600,
        'departure_time': '23:45',
        'arrival_time': '18:25',
        'departure_station': 'Chennai Central',
        'arrival_station': 'Mumbai CST',
        'duration': '18h 40m',
        'frequency': 'Daily',
        'class_available': 'SL, 3A, 2A, 1A',
        'schedule': [
            {'station': 'Chennai Central', 'arrival': '--', 'departure': '23:45', 'platform': '6'},
            {'station': 'Arakkonam', 'arrival': '00:53', 'departure': '00:55', 'platform': '3'},
            {'station': 'Katpadi Junction', 'arrival': '01:28', 'departure': '01:30', 'platform': '4'},
            {'station': 'Mumbai CST', 'arrival': '18:25', 'departure': '--', 'platform': '18'}
        ]
    },
    {
        'number': '12841', 
        'name': 'Coromandel Express', 
        'route': 'Chennai - Howrah', 
        'seats': 550,
        'departure_time': '08:40',
        'arrival_time': '11:05',
        'departure_station': 'Chennai Central',
        'arrival_station': 'Howrah Junction',
        'duration': '26h 25m',
        'frequency': 'Daily',
        'class_available': 'SL, 3A, 2A, 1A',
        'schedule': [
            {'station': 'Chennai Central', 'arrival': '--', 'departure': '08:40', 'platform': '9'},
            {'station': 'Arakkonam', 'arrival': '09:48', 'departure': '09:50', 'platform': '2'},
            {'station': 'Katpadi Junction', 'arrival': '10:23', 'departure': '10:25', 'platform': '3'},
            {'station': 'Howrah Junction', 'arrival': '11:05', 'departure': '--', 'platform': '23'}
        ]
    },
    {
        'number': '16053', 
        'name': 'Rock Fort Express', 
        'route': 'Trichy - Chennai', 
        'seats': 400,
        'departure_time': '20:30',
        'arrival_time': '05:00',
        'departure_station': 'Trichy Junction',
        'arrival_station': 'Chennai Central',
        'duration': '8h 30m',
        'frequency': 'Daily',
        'class_available': 'SL, 3A, 2A',
        'schedule': [
            {'station': 'Trichy Junction', 'arrival': '--', 'departure': '20:30', 'platform': '4'},
            {'station': 'Villupuram Junction', 'arrival': '23:05', 'departure': '23:10', 'platform': '3'},
            {'station': 'Chengalpattu', 'arrival': '03:30', 'departure': '03:32', 'platform': '2'},
            {'station': 'Tambaram', 'arrival': '04:25', 'departure': '04:27', 'platform': '3'},
            {'station': 'Chennai Central', 'arrival': '05:00', 'departure': '--', 'platform': '8'}
        ]
    },
    {
        'number': '12661', 
        'name': 'Pearl City Express', 
        'route': 'Chennai - Tuticorin', 
        'seats': 380,
        'departure_time': '21:30',
        'arrival_time': '08:30',
        'departure_station': 'Chennai Egmore',
        'arrival_station': 'Tuticorin',
        'duration': '11h 00m',
        'frequency': 'Daily',
        'class_available': 'SL, 3A, 2A',
        'schedule': [
            {'station': 'Chennai Egmore', 'arrival': '--', 'departure': '21:30', 'platform': '4'},
            {'station': 'Villupuram Junction', 'arrival': '23:50', 'departure': '23:55', 'platform': '2'},
            {'station': 'Trichy Junction', 'arrival': '02:30', 'departure': '02:35', 'platform': '3'},
            {'station': 'Madurai Junction', 'arrival': '05:15', 'departure': '05:20', 'platform': '4'},
            {'station': 'Tuticorin', 'arrival': '08:30', 'departure': '--', 'platform': '1'}
        ]
    },
    {
        'number': '16101', 
        'name': 'Rameswaram Express', 
        'route': 'Chennai - Rameswaram', 
        'seats': 420,
        'departure_time': '20:50',
        'arrival_time': '07:30',
        'departure_station': 'Chennai Egmore',
        'arrival_station': 'Rameswaram',
        'duration': '10h 40m',
        'frequency': 'Daily',
        'class_available': 'SL, 3A, 2A',
        'schedule': [
            {'station': 'Chennai Egmore', 'arrival': '--', 'departure': '20:50', 'platform': '6'},
            {'station': 'Chengalpattu', 'arrival': '21:50', 'departure': '21:52', 'platform': '1'},
            {'station': 'Villupuram Junction', 'arrival': '23:20', 'departure': '23:25', 'platform': '4'},
            {'station': 'Trichy Junction', 'arrival': '02:15', 'departure': '02:20', 'platform': '2'},
            {'station': 'Madurai Junction', 'arrival': '05:00', 'departure': '05:05', 'platform': '3'},
            {'station': 'Rameswaram', 'arrival': '07:30', 'departure': '--', 'platform': '1'}
        ]
    },
    {
        'number': '12633', 
        'name': 'Kanyakumari Express', 
        'route': 'Chennai - Kanyakumari', 
        'seats': 450,
        'departure_time': '17:30',
        'arrival_time': '06:00',
        'departure_station': 'Chennai Egmore',
        'arrival_station': 'Kanyakumari',
        'duration': '12h 30m',
        'frequency': 'Daily',
        'class_available': 'SL, 3A, 2A, 1A',
        'schedule': [
            {'station': 'Chennai Egmore', 'arrival': '--', 'departure': '17:30', 'platform': '2'},
            {'station': 'Villupuram Junction', 'arrival': '19:50', 'departure': '19:55', 'platform': '3'},
            {'station': 'Trichy Junction', 'arrival': '22:35', 'departure': '22:40', 'platform': '4'},
            {'station': 'Madurai Junction', 'arrival': '01:15', 'departure': '01:20', 'platform': '5'},
            {'station': 'Nagercoil Junction', 'arrival': '05:00', 'departure': '05:05', 'platform': '2'},
            {'station': 'Kanyakumari', 'arrival': '06:00', 'departure': '--', 'platform': '1'}
        ]
    }
]

def get_db():
    conn = sqlite3.connect('railway.db')
    conn.row_factory = sqlite3.Row
    return conn

def generate_pnr():
    return ''.join(random.choices(string.digits, k=10))

# API endpoints
@app.route('/api/stations')
def api_stations():
    return jsonify(STATIONS)

@app.route('/api/platforms/<station>')
def api_platforms(station):
    platforms = PLATFORMS.get(station, ['1', '2'])
    return jsonify(platforms)

@app.route('/api/trains')
def api_trains():
    return jsonify(TRAINS)

@app.route('/api/train-schedule/<train_number>')
def api_train_schedule(train_number):
    for train in TRAINS:
        if train['number'] == train_number:
            return jsonify(train)
    return jsonify({'error': 'Train not found'}), 404

@app.route('/api/train-availability')
def api_train_availability():
    conn = get_db()
    bookings = conn.execute('''
        SELECT train_name, COUNT(*) as booked 
        FROM ticket_bookings 
        GROUP BY train_name
    ''').fetchall()
    conn.close()
    
    availability = []
    for train in TRAINS:
        train_full_name = f"{train['name']} - {train['number']}"
        booked = 0
        for booking in bookings:
            if train['number'] in booking['train_name'] or train['name'] in booking['train_name']:
                booked = booking['booked']
                break
        
        available = train['seats'] - booked
        availability.append({
            'number': train['number'],
            'name': train['name'],
            'route': train['route'],
            'total_seats': train['seats'],
            'booked': booked,
            'available': available,
            'percentage': round((booked / train['seats']) * 100, 2),
            'departure_time': train['departure_time'],
            'arrival_time': train['arrival_time'],
            'duration': train['duration']
        })
    
    return jsonify(availability)

# Home Page
@app.route('/')
def index():
    return render_template('index.html')

# Admin Login
@app.route('/admin/login', methods=['GET', 'POST'])
def admin_login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        password_hash = hashlib.sha256(password.encode()).hexdigest()
        
        conn = get_db()
        admin = conn.execute('SELECT * FROM admin WHERE username = ? AND password = ?',
                            (username, password_hash)).fetchone()
        conn.close()
        
        if admin:
            session['admin_logged_in'] = True
            session['admin_username'] = username
            flash('Login successful!', 'success')
            return redirect(url_for('admin_dashboard'))
        else:
            flash('Invalid credentials!', 'danger')
    
    return render_template('admin_login.html')

# Admin Dashboard
@app.route('/admin/dashboard')
def admin_dashboard():
    if not session.get('admin_logged_in'):
        return redirect(url_for('admin_login'))
    
    conn = get_db()
    
    total_crowd_updates = conn.execute('SELECT COUNT(*) as count FROM crowd_updates').fetchone()['count']
    total_emergencies = conn.execute('SELECT COUNT(*) as count FROM emergency_alerts').fetchone()['count']
    total_tickets = conn.execute('SELECT COUNT(*) as count FROM ticket_bookings').fetchone()['count']
    pending_emergencies = conn.execute('SELECT COUNT(*) as count FROM emergency_alerts WHERE status = "Pending"').fetchone()['count']
    total_women_alerts = conn.execute('SELECT COUNT(*) as count FROM women_safety_alerts').fetchone()['count']
    
    recent_crowds = conn.execute('SELECT * FROM crowd_updates ORDER BY update_time DESC LIMIT 5').fetchall()
    recent_emergencies = conn.execute('SELECT * FROM emergency_alerts ORDER BY alert_time DESC LIMIT 5').fetchall()
    
    conn.close()
    
    return render_template('admin_dashboard.html',
                         total_crowd_updates=total_crowd_updates,
                         total_emergencies=total_emergencies,
                         total_tickets=total_tickets,
                         pending_emergencies=pending_emergencies,
                         total_women_alerts=total_women_alerts,
                         recent_crowds=recent_crowds,
                         recent_emergencies=recent_emergencies)

# Admin Logout
@app.route('/admin/logout')
def admin_logout():
    session.clear()
    flash('Logged out successfully!', 'info')
    return redirect(url_for('index'))

# Crowd Update Page
@app.route('/admin/crowd-update', methods=['GET', 'POST'])
def crowd_update():
    if not session.get('admin_logged_in'):
        return redirect(url_for('admin_login'))
    
    if request.method == 'POST':
        station_name = request.form['station_name']
        crowd_level = request.form['crowd_level']
        platform_no = request.form['platform_no']
        train_name = request.form['train_name']
        remarks = request.form['remarks']
        
        block_data = {
            'type': 'crowd_update',
            'station': station_name,
            'crowd_level': crowd_level,
            'platform': platform_no,
            'train': train_name,
            'timestamp': str(datetime.now())
        }
        blockchain_hash = railway_blockchain.add_block(block_data)
        
        conn = get_db()
        conn.execute('''INSERT INTO crowd_updates 
                       (station_name, crowd_level, platform_no, train_name, remarks, updated_by, blockchain_hash)
                       VALUES (?, ?, ?, ?, ?, ?, ?)''',
                    (station_name, crowd_level, platform_no, train_name, remarks, 
                     session['admin_username'], blockchain_hash))
        conn.commit()
        conn.close()
        
        flash('Crowd update added successfully!', 'success')
        return redirect(url_for('crowd_update'))
    
    conn = get_db()
    crowd_updates = conn.execute('SELECT * FROM crowd_updates ORDER BY update_time DESC').fetchall()
    conn.close()
    
    return render_template('crowd_update.html', 
                         crowd_updates=crowd_updates,
                         stations=STATIONS,
                         trains=TRAINS)

# View All Alerts (Admin)
@app.route('/admin/alerts')
def admin_alerts():
    if not session.get('admin_logged_in'):
        return redirect(url_for('admin_login'))
    
    conn = get_db()
    emergency_alerts = conn.execute('SELECT * FROM emergency_alerts ORDER BY alert_time DESC').fetchall()
    women_alerts = conn.execute('SELECT * FROM women_safety_alerts ORDER BY alert_time DESC').fetchall()
    conn.close()
    
    return render_template('admin_alerts.html',
                         emergency_alerts=emergency_alerts,
                         women_alerts=women_alerts)

# Update Alert Status
@app.route('/admin/update-alert-status/<alert_type>/<int:alert_id>/<status>')
def update_alert_status(alert_type, alert_id, status):
    if not session.get('admin_logged_in'):
        return redirect(url_for('admin_login'))
    
    conn = get_db()
    if alert_type == 'emergency':
        conn.execute('UPDATE emergency_alerts SET status = ? WHERE id = ?', (status, alert_id))
    elif alert_type == 'women':
        conn.execute('UPDATE women_safety_alerts SET status = ? WHERE id = ?', (status, alert_id))
    conn.commit()
    conn.close()
    
    flash(f'Alert status updated to {status}!', 'success')
    return redirect(url_for('admin_alerts'))

# View Blockchain
@app.route('/admin/blockchain')
def admin_blockchain():
    if not session.get('admin_logged_in'):
        return redirect(url_for('admin_login'))
    
    blocks = []
    for block in railway_blockchain.chain:
        blocks.append({
            'index': block.index,
            'timestamp': block.timestamp,
            'data': block.data,
            'hash': block.hash,
            'previous_hash': block.previous_hash
        })
    
    is_valid = railway_blockchain.is_chain_valid()
    
    return render_template('admin_blockchain.html',
                         blocks=blocks,
                         is_valid=is_valid,
                         total_blocks=len(blocks))

# Train Availability (Admin)
@app.route('/admin/train-availability')
def admin_train_availability():
    if not session.get('admin_logged_in'):
        return redirect(url_for('admin_login'))
    
    return render_template('admin_train_availability.html', trains=TRAINS)

# Train Schedule (Admin & Passenger)
@app.route('/train-schedule')
def train_schedule():
    return render_template('train_schedule.html', trains=TRAINS)

@app.route('/train-schedule/<train_number>')
def train_schedule_detail(train_number):
    train = None
    for t in TRAINS:
        if t['number'] == train_number:
            train = t
            break
    
    if not train:
        flash('Train not found!', 'danger')
        return redirect(url_for('train_schedule'))
    
    return render_template('train_schedule_detail.html', train=train)

# Passenger View Page
@app.route('/passenger/view')
def passenger_view():
    conn = get_db()
    crowd_updates = conn.execute('SELECT * FROM crowd_updates ORDER BY update_time DESC LIMIT 50').fetchall()
    conn.close()
    
    return render_template('passenger_view.html', crowd_updates=crowd_updates)

# Train Availability (Passenger)
@app.route('/passenger/train-availability')
def passenger_train_availability():
    return render_template('passenger_train_availability.html', trains=TRAINS)

# Emergency Alert Page
@app.route('/passenger/emergency', methods=['GET', 'POST'])
def emergency_alert():
    if request.method == 'POST':
        passenger_name = request.form['passenger_name']
        phone = request.form['phone']
        location = request.form['location']
        emergency_type = request.form['emergency_type']
        description = request.form['description']
        
        block_data = {
            'type': 'emergency_alert',
            'passenger': passenger_name,
            'location': location,
            'emergency_type': emergency_type,
            'timestamp': str(datetime.now())
        }
        blockchain_hash = railway_blockchain.add_block(block_data)
        
        conn = get_db()
        conn.execute('''INSERT INTO emergency_alerts 
                       (passenger_name, phone, location, emergency_type, description, blockchain_hash)
                       VALUES (?, ?, ?, ?, ?, ?)''',
                    (passenger_name, phone, location, emergency_type, description, blockchain_hash))
        conn.commit()
        conn.close()
        
        try:
            msg = Message('Emergency Alert - Railway System',
                         recipients=['eslineslin333@gmail.com'])
            msg.body = f'''
            Emergency Alert Received!
            
            Passenger: {passenger_name}
            Phone: {phone}
            Location: {location}
            Type: {emergency_type}
            Description: {description}
            Time: {datetime.now()}
            '''
            mail.send(msg)
        except:
            pass
        
        flash('Emergency alert sent successfully! Authorities have been notified.', 'success')
        return redirect(url_for('emergency_alert'))
    
    return render_template('emergency_alert.html')

# Women Safety Alert Page
@app.route('/passenger/women-safety', methods=['GET', 'POST'])
def women_safety():
    if request.method == 'POST':
        passenger_name = request.form['passenger_name']
        phone = request.form['phone']
        train_no = request.form['train_no']
        coach_no = request.form['coach_no']
        location = request.form['location']
        description = request.form['description']
        
        block_data = {
            'type': 'women_safety_alert',
            'passenger': passenger_name,
            'train': train_no,
            'coach': coach_no,
            'location': location,
            'timestamp': str(datetime.now())
        }
        blockchain_hash = railway_blockchain.add_block(block_data)
        
        conn = get_db()
        conn.execute('''INSERT INTO women_safety_alerts 
                       (passenger_name, phone, train_no, coach_no, location, description, blockchain_hash)
                       VALUES (?, ?, ?, ?, ?, ?, ?)''',
                    (passenger_name, phone, train_no, coach_no, location, description, blockchain_hash))
        conn.commit()
        conn.close()
        
        try:
            msg = Message('URGENT: Women Safety Alert - Railway System',
                         recipients=['railway_police@gmail.com','eslineslin333@gmail.com'])
            msg.body = f'''
            URGENT WOMEN SAFETY ALERT!
            
            Passenger: {passenger_name}
            Phone: {phone}
            Train Number: {train_no}
            Coach: {coach_no}
            Location: {location}
            Description: {description}
            Time: {datetime.now()}
            
            IMMEDIATE ACTION REQUIRED!
            '''
            mail.send(msg)
        except:
            pass
        
        flash('Safety alert sent! Police and railway security have been notified.', 'success')
        return redirect(url_for('women_safety'))
    
    return render_template('women_safety.html')

# Ticket Booking Page
@app.route('/passenger/ticket-booking', methods=['GET', 'POST'])
def ticket_booking():
    if request.method == 'POST':
        passenger_name = request.form['passenger_name']
        age = request.form['age']
        gender = request.form['gender']
        phone = request.form['phone']
        email = request.form['email']
        from_station = request.form['from_station']
        to_station = request.form['to_station']
        journey_date = request.form['journey_date']
        train_name = request.form['train_name']
        ticket_price = request.form['ticket_price']
        
        pnr_number = generate_pnr()
        
        block_data = {
            'type': 'ticket_booking',
            'pnr': pnr_number,
            'passenger': passenger_name,
            'from': from_station,
            'to': to_station,
            'date': journey_date,
            'timestamp': str(datetime.now())
        }
        blockchain_hash = railway_blockchain.add_block(block_data)
        
        conn = get_db()
        conn.execute('''INSERT INTO ticket_bookings 
                       (passenger_name, age, gender, phone, email, from_station, to_station, 
                        journey_date, train_name, ticket_price, pnr_number, blockchain_hash)
                       VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)''',
                    (passenger_name, age, gender, phone, email, from_station, to_station,
                     journey_date, train_name, ticket_price, pnr_number, blockchain_hash))
        conn.commit()
        conn.close()
        
        try:
            msg = Message('Ticket Booking Confirmation',
                         recipients=[email])
            msg.body = f'''
            Dear {passenger_name},
            
            Your ticket has been booked successfully!
            
            PNR Number: {pnr_number}
            From: {from_station}
            To: {to_station}
            Date: {journey_date}
            Train: {train_name}
            Price: ₹{ticket_price}
            
            Thank you for using our service!
            '''
            mail.send(msg)
        except:
            pass
        
        flash(f'Ticket booked successfully! Your PNR: {pnr_number}', 'success')
        return redirect(url_for('ticket_booking'))
    
    return render_template('ticket_booking.html', stations=STATIONS, trains=TRAINS)

# Destination Alert Page
@app.route('/passenger/destination-alert', methods=['GET', 'POST'])
def destination_alert():
    if request.method == 'POST':
        passenger_name = request.form['passenger_name']
        phone = request.form['phone']
        email = request.form['email']
        destination_station = request.form['destination_station']
        train_name = request.form['train_name']
        
        conn = get_db()
        conn.execute('''INSERT INTO destination_alerts 
                       (passenger_name, phone, email, destination_station, train_name)
                       VALUES (?, ?, ?, ?, ?)''',
                    (passenger_name, phone, email, destination_station, train_name))
        conn.commit()
        conn.close()
        
        try:
            msg = Message('Destination Alert Registered',
                         recipients=[email])
            msg.body = f'''
            Dear {passenger_name},
            
            You will receive an alert when approaching {destination_station}.
            Train: {train_name}
            
            Have a safe journey!
            '''
            mail.send(msg)
        except:
            pass
        
        flash('Destination alert registered! You will be notified.', 'success')
        return redirect(url_for('destination_alert'))
    
    return render_template('destination_alert.html', stations=STATIONS, trains=TRAINS)

# Generate PDF Report
@app.route('/admin/generate-report')
def generate_report():
    if not session.get('admin_logged_in'):
        return redirect(url_for('admin_login'))
    
    from datetime import datetime, timedelta
    
    conn = get_db()
    
    # Date range
    today = datetime.now()
    last_month = today - timedelta(days=30)
    last_week = today - timedelta(days=7)
    
    # All statistics
    report_data = {
        'generated_on': today.strftime('%Y-%m-%d %H:%M:%S'),
        'period_start': last_month.strftime('%Y-%m-%d'),
        'period_end': today.strftime('%Y-%m-%d'),
        
        # Overview Stats
        'total_crowd_updates': conn.execute('SELECT COUNT(*) as count FROM crowd_updates WHERE update_time >= ?', (last_month,)).fetchone()['count'],
        'total_emergencies': conn.execute('SELECT COUNT(*) as count FROM emergency_alerts WHERE alert_time >= ?', (last_month,)).fetchone()['count'],
        'total_women_alerts': conn.execute('SELECT COUNT(*) as count FROM women_safety_alerts WHERE alert_time >= ?', (last_month,)).fetchone()['count'],
        'total_tickets': conn.execute('SELECT COUNT(*) as count FROM ticket_bookings WHERE booking_time >= ?', (last_month,)).fetchone()['count'],
        'total_revenue': conn.execute('SELECT SUM(ticket_price) as total FROM ticket_bookings WHERE booking_time >= ?', (last_month,)).fetchone()['total'] or 0,
        
        # Detailed Data
        'crowd_by_station': conn.execute('''
            SELECT station_name, crowd_level, COUNT(*) as count 
            FROM crowd_updates 
            WHERE update_time >= ?
            GROUP BY station_name, crowd_level
            ORDER BY station_name, crowd_level
        ''', (last_month,)).fetchall(),
        
        'emergency_by_type': conn.execute('''
            SELECT emergency_type, status, COUNT(*) as count 
            FROM emergency_alerts 
            WHERE alert_time >= ?
            GROUP BY emergency_type, status
            ORDER BY count DESC
        ''', (last_month,)).fetchall(),
        
        'top_trains': conn.execute('''
            SELECT train_name, COUNT(*) as bookings, SUM(ticket_price) as revenue
            FROM ticket_bookings 
            WHERE booking_time >= ?
            GROUP BY train_name
            ORDER BY bookings DESC
            LIMIT 10
        ''', (last_month,)).fetchall(),
        
        'daily_bookings': conn.execute('''
            SELECT DATE(booking_time) as date, COUNT(*) as count, SUM(ticket_price) as revenue
            FROM ticket_bookings 
            WHERE booking_time >= ?
            GROUP BY DATE(booking_time)
            ORDER BY date DESC
        ''', (last_month,)).fetchall(),
        
        'women_safety_stats': conn.execute('''
            SELECT status, COUNT(*) as count 
            FROM women_safety_alerts 
            WHERE alert_time >= ?
            GROUP BY status
        ''', (last_month,)).fetchall(),
        
        # Recent activities
        'recent_bookings': conn.execute('''
            SELECT * FROM ticket_bookings 
            WHERE booking_time >= ?
            ORDER BY booking_time DESC 
            LIMIT 20
        ''', (last_week,)).fetchall(),
        
        'recent_alerts': conn.execute('''
            SELECT * FROM emergency_alerts 
            WHERE alert_time >= ?
            ORDER BY alert_time DESC 
            LIMIT 20
        ''', (last_week,)).fetchall(),
    }
    
    conn.close()
    
    return render_template('admin_report_generate.html', report=report_data)

# Admin Reports
@app.route('/admin/reports')
def admin_reports():
    if not session.get('admin_logged_in'):
        return redirect(url_for('admin_login'))
    
    conn = get_db()
    
    today = datetime.now()
    last_month = today - timedelta(days=30)
    
    crowd_by_station = conn.execute('''
        SELECT station_name, crowd_level, COUNT(*) as count 
        FROM crowd_updates 
        WHERE update_time >= ?
        GROUP BY station_name, crowd_level
        ORDER BY count DESC
    ''', (last_month,)).fetchall()
    
    emergency_by_type = conn.execute('''
        SELECT emergency_type, COUNT(*) as count 
        FROM emergency_alerts 
        WHERE alert_time >= ?
        GROUP BY emergency_type
        ORDER BY count DESC
    ''', (last_month,)).fetchall()
    
    bookings_by_date = conn.execute('''
        SELECT DATE(booking_time) as date, COUNT(*) as count, SUM(ticket_price) as revenue
        FROM ticket_bookings 
        WHERE booking_time >= ?
        GROUP BY DATE(booking_time)
        ORDER BY date DESC
    ''', (last_month,)).fetchall()
    
    popular_trains = conn.execute('''
        SELECT train_name, COUNT(*) as bookings, SUM(ticket_price) as revenue
        FROM ticket_bookings 
        WHERE booking_time >= ?
        GROUP BY train_name
        ORDER BY bookings DESC
        LIMIT 10
    ''', (last_month,)).fetchall()
    
    women_alerts_stats = conn.execute('''
        SELECT status, COUNT(*) as count 
        FROM women_safety_alerts 
        WHERE alert_time >= ?
        GROUP BY status
    ''', (last_month,)).fetchall()
    
    total_revenue = conn.execute('''
        SELECT SUM(ticket_price) as total 
        FROM ticket_bookings 
        WHERE booking_time >= ?
    ''', (last_month,)).fetchone()['total'] or 0
    
    total_bookings = conn.execute('''
        SELECT COUNT(*) as count 
        FROM ticket_bookings 
        WHERE booking_time >= ?
    ''', (last_month,)).fetchone()['count']
    
    total_alerts = conn.execute('''
        SELECT COUNT(*) as count 
        FROM emergency_alerts 
        WHERE alert_time >= ?
    ''', (last_month,)).fetchone()['count']
    
    conn.close()
    
    return render_template('admin_reports.html',
                         crowd_by_station=crowd_by_station,
                         emergency_by_type=emergency_by_type,
                         bookings_by_date=bookings_by_date,
                         popular_trains=popular_trains,
                         women_alerts_stats=women_alerts_stats,
                         total_revenue=total_revenue,
                         total_bookings=total_bookings,
                         total_alerts=total_alerts,
                         last_month=last_month.strftime('%Y-%m-%d'),
                         today=today.strftime('%Y-%m-%d'))

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)
