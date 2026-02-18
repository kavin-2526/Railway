import sqlite3
import os

# Check if database exists
if os.path.exists('railway.db'):
    print("✅ Database file exists")
    
    # Check if tables exist
    conn = sqlite3.connect('railway.db')
    cursor = conn.cursor()
    
    cursor.execute("SELECT name FROM sqlite_master WHERE type='table'")
    tables = cursor.fetchall()
    
    print(f"Found {len(tables)} tables:")
    for table in tables:
        print(f"  - {table[0]}")
    
    # Check for essential tables
    essential_tables = ['admin', 'crowd_updates', 'emergency_alerts', 'ticket_bookings']
    missing_tables = [table for table in essential_tables if table not in [t[0] for t in tables]]
    
    if missing_tables:
        print(f"❌ Missing tables: {missing_tables}")
        print("You need to run db_init.py")
    else:
        print("✅ All essential tables exist")
        print("You DON'T need to run db_init.py")
    
    conn.close()
else:
    print("❌ Database file doesn't exist")
    print("You NEED to run db_init.py")