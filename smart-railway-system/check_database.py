import sqlite3
import os

# Check if database exists
if os.path.exists('railway.db'):
    print("✅ Database file exists!")
    
    # Connect and check tables
    conn = sqlite3.connect('railway.db')
    cursor = conn.cursor()
    
    # Get all tables
    cursor.execute("SELECT name FROM sqlite_master WHERE type='table'")
    tables = cursor.fetchall()
    
    print(f"\n📊 Found {len(tables)} tables:")
    for table in tables:
        print(f"  ✅ {table[0]}")
        
        # Count records in each table
        cursor.execute(f"SELECT COUNT(*) FROM {table[0]}")
        count = cursor.fetchone()[0]
        print(f"     Records: {count}")
    
    # Check admin user
    cursor.execute("SELECT username FROM admin")
    admin = cursor.fetchone()
    if admin:
        print(f"\n👤 Default admin user: {admin[0]}")
    
    conn.close()
    print("\n✅ Database is ready to use!")
else:
    print("❌ Database file not found. Running initialization...")
    import database
    database.init_db()