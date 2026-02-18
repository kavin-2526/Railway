import sqlite3
from datetime import datetime
import hashlib

def init_db():
    print("🔄 Starting database initialization...")
    
    try:
        conn = sqlite3.connect('railway.db')
        c = conn.cursor()
        print("✅ Database connection established")
        
        # Admin table
        print("📋 Creating admin table...")
        c.execute('''CREATE TABLE IF NOT EXISTS admin
                     (id INTEGER PRIMARY KEY AUTOINCREMENT,
                      username TEXT UNIQUE NOT NULL,
                      password TEXT NOT NULL,
                      email TEXT,
                      created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP)''')
        print("✅ Admin table created")
        
        # Crowd updates table
        print("📋 Creating crowd_updates table...")
        c.execute('''CREATE TABLE IF NOT EXISTS crowd_updates
                     (id INTEGER PRIMARY KEY AUTOINCREMENT,
                      station_name TEXT NOT NULL,
                      crowd_level TEXT NOT NULL,
                      platform_no TEXT,
                      train_name TEXT,
                      remarks TEXT,
                      updated_by TEXT,
                      update_time TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                      blockchain_hash TEXT)''')
        print("✅ Crowd updates table created")
        
        # Emergency alerts table
        print("📋 Creating emergency_alerts table...")
        c.execute('''CREATE TABLE IF NOT EXISTS emergency_alerts
                     (id INTEGER PRIMARY KEY AUTOINCREMENT,
                      passenger_name TEXT NOT NULL,
                      phone TEXT NOT NULL,
                      location TEXT NOT NULL,
                      emergency_type TEXT NOT NULL,
                      description TEXT,
                      status TEXT DEFAULT 'Pending',
                      alert_time TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                      blockchain_hash TEXT)''')
        print("✅ Emergency alerts table created")
        
        # Women safety alerts table
        print("📋 Creating women_safety_alerts table...")
        c.execute('''CREATE TABLE IF NOT EXISTS women_safety_alerts
                     (id INTEGER PRIMARY KEY AUTOINCREMENT,
                      passenger_name TEXT NOT NULL,
                      phone TEXT NOT NULL,
                      train_no TEXT,
                      coach_no TEXT,
                      location TEXT NOT NULL,
                      description TEXT,
                      police_notified TEXT DEFAULT 'Yes',
                      status TEXT DEFAULT 'Active',
                      alert_time TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                      blockchain_hash TEXT)''')
        print("✅ Women safety alerts table created")
        
        # Ticket bookings table
        print("📋 Creating ticket_bookings table...")
        c.execute('''CREATE TABLE IF NOT EXISTS ticket_bookings
                     (id INTEGER PRIMARY KEY AUTOINCREMENT,
                      passenger_name TEXT NOT NULL,
                      age INTEGER,
                      gender TEXT,
                      phone TEXT NOT NULL,
                      email TEXT,
                      from_station TEXT NOT NULL,
                      to_station TEXT NOT NULL,
                      journey_date TEXT NOT NULL,
                      train_name TEXT,
                      ticket_price REAL,
                      booking_time TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                      pnr_number TEXT UNIQUE,
                      blockchain_hash TEXT)''')
        print("✅ Ticket bookings table created")
        
        # Destination alerts table
        print("📋 Creating destination_alerts table...")
        c.execute('''CREATE TABLE IF NOT EXISTS destination_alerts
                     (id INTEGER PRIMARY KEY AUTOINCREMENT,
                      passenger_name TEXT NOT NULL,
                      phone TEXT NOT NULL,
                      email TEXT,
                      destination_station TEXT NOT NULL,
                      train_name TEXT,
                      alert_sent TEXT DEFAULT 'No',
                      created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP)''')
        print("✅ Destination alerts table created")
        
        # Insert default admin if not exists
        print("👤 Creating default admin user...")
        try:
            password_hash = hashlib.sha256('admin123'.encode()).hexdigest()
            c.execute("INSERT INTO admin (username, password, email) VALUES (?, ?, ?)",
                      ('admin', password_hash, 'admin@railway.com'))
            print("✅ Default admin user created")
        except sqlite3.IntegrityError:
            print("ℹ️  Admin user already exists")
        
        conn.commit()
        print("💾 Changes committed to database")
        
        # Verify tables
        c.execute("SELECT name FROM sqlite_master WHERE type='table'")
        tables = c.fetchall()
        print(f"\n✅ Database initialized successfully!")
        print(f"📊 Total tables created: {len(tables)}")
        for table in tables:
            print(f"   - {table[0]}")
        
        conn.close()
        print("\n🎉 Database setup complete!")
        print("📁 File location: railway.db")
        print("👤 Default login - Username: admin | Password: admin123")
        
    except Exception as e:
        print(f"\n❌ Error during initialization: {e}")
        import traceback
        traceback.print_exc()


if __name__ == '__main__':
    init_db()