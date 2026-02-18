import sqlite3
from datetime import datetime, timedelta
import random
import hashlib

def add_sample_data():
    print("🔄 Adding sample Tamil Nadu railway data...")
    
    conn = sqlite3.connect('railway.db')
    c = conn.cursor()
    
    # Sample Crowd Updates
    crowd_data = [
        ('Chennai Central', 'High', '1', 'Coromandel Express - 12841', 'Heavy morning rush, passengers advised to arrive early', 'admin'),
        ('Chennai Egmore', 'Medium', '3', 'Pandian Express - 12617', 'Moderate crowd, ticket counters operational', 'admin'),
        ('Tambaram', 'High', '2', 'Chennai Beach MEMU - 43501', 'Local train crowd, peak office hours', 'admin'),
        ('Tiruppur', 'Low', '1', 'Kovai Express - 12676', 'Comfortable travel, less crowded', 'admin'),
        ('Coimbatore Junction', 'Medium', '4', 'Nilgiri Express - 12671', 'Moderate crowd, platforms clean and accessible', 'admin'),
        ('Madurai Junction', 'Low', '2', 'Vaigai Express - 12635', 'Off-peak hours, comfortable boarding', 'admin'),
        ('Trichy Junction', 'Medium', '3', 'Rock Fort Express - 16053', 'Steady passenger flow, food courts available', 'admin'),
        ('Salem Junction', 'Low', '1', 'Salem Express - 11042', 'Less crowded, all amenities functional', 'admin'),
        ('Erode Junction', 'Medium', '2', 'Cheran Express - 12673', 'Normal crowd levels, ticket booking smooth', 'admin'),
        ('Chennai Central', 'High', '5', 'Brindavan Express - 12639', 'Evening peak hour rush, long queues at platforms', 'admin'),
        ('Kanchipuram', 'Medium', '1', 'MEMU Local - 66011', 'Temple town evening crowd, manageable', 'admin'),
        ('Villupuram Junction', 'Low', '4', 'Pondicherry Express - 12665', 'Comfortable boarding conditions', 'admin'),
        ('Nagercoil Junction', 'Medium', '2', 'Kanyakumari Express - 12633', 'Tourist season, moderate crowd levels', 'admin'),
        ('Rameswaram', 'High', '1', 'Rameswaram Express - 16101', 'Pilgrimage rush, extra staff deployed', 'admin'),
        ('Thanjavur', 'Low', '1', 'Thanjavur Express - 16187', 'Peaceful night departure, less crowded', 'admin'),
    ]
    
    print(f"📊 Adding {len(crowd_data)} crowd updates...")
    for data in crowd_data:
        # Generate blockchain hash
        block_data = f"{data[0]}-{data[1]}-{datetime.now()}"
        blockchain_hash = hashlib.sha256(block_data.encode()).hexdigest()
        
        c.execute('''INSERT INTO crowd_updates 
                    (station_name, crowd_level, platform_no, train_name, remarks, updated_by, blockchain_hash)
                    VALUES (?, ?, ?, ?, ?, ?, ?)''',
                 (*data, blockchain_hash))
    
    print("✅ Crowd updates added!")
    
    # Sample Ticket Bookings
    tomorrow = (datetime.now() + timedelta(days=1)).strftime('%Y-%m-%d')
    
    ticket_data = [
        ('Rajesh Kumar', 35, 'Male', '9876543210', 'rajesh.kumar@gmail.com', 
         'Chennai Central', 'Coimbatore Junction', tomorrow, 'Kovai Express - 12676', 350),
        ('Priya Sivakumar', 28, 'Female', '9845612378', 'priya.siva@gmail.com',
         'Madurai Junction', 'Chennai Egmore', tomorrow, 'Pandian Express - 12617', 150),
        ('Murugan Natarajan', 45, 'Male', '9789456123', 'murugan.n@yahoo.com',
         'Trichy Junction', 'Bangalore City', tomorrow, 'Kaveri Express - 16021', 550),
        ('Lakshmi Iyer', 32, 'Female', '9965874123', 'lakshmi.iyer@outlook.com',
         'Salem Junction', 'Chennai Central', tomorrow, 'Salem Express - 11042', 50),
        ('Karthi Selvam', 26, 'Male', '9874563210', 'karthi.s@gmail.com',
         'Tiruppur', 'Erode Junction', tomorrow, 'Nilgiri Express - 12671', 50),
        ('Anitha Ramesh', 29, 'Female', '9123456789', 'anitha.r@gmail.com',
         'Chennai Egmore', 'Madurai Junction', tomorrow, 'Vaigai Express - 12635', 150),
        ('Senthil Kumar', 38, 'Male', '9988776655', 'senthil.k@yahoo.com',
         'Coimbatore Junction', 'Chennai Central', tomorrow, 'Shatabdi Express - 12028', 950),
        ('Divya Krishnan', 24, 'Female', '9445566778', 'divya.k@gmail.com',
         'Villupuram Junction', 'Chennai Central', tomorrow, 'Pondicherry Express - 12665', 50),
    ]
    
    print(f"🎫 Adding {len(ticket_data)} ticket bookings...")
    for data in ticket_data:
        # Generate PNR
        pnr = ''.join([str(random.randint(0, 9)) for _ in range(10)])
        
        # Generate blockchain hash
        block_data = f"{data[0]}-{pnr}-{datetime.now()}"
        blockchain_hash = hashlib.sha256(block_data.encode()).hexdigest()
        
        c.execute('''INSERT INTO ticket_bookings 
                    (passenger_name, age, gender, phone, email, from_station, to_station, 
                     journey_date, train_name, ticket_price, pnr_number, blockchain_hash)
                    VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)''',
                 (*data, pnr, blockchain_hash))
    
    print("✅ Ticket bookings added!")
    
    # Sample Destination Alerts
    alert_data = [
        ('Vijay Prakash', '9876501234', 'vijay.p@gmail.com', 'Coimbatore Junction', 'Shatabdi Express - 12028'),
        ('Meena Sundaram', '9789012345', 'meena.s@gmail.com', 'Chennai Central', 'Vaigai Express - 12635'),
        ('Kumar Rajan', '9654321098', 'kumar.r@gmail.com', 'Madurai Junction', 'Pandian Express - 12617'),
        ('Sangeetha Devi', '9543210987', 'sangeetha.d@outlook.com', 'Salem Junction', 'Salem Express - 11042'),
    ]
    
    print(f"📍 Adding {len(alert_data)} destination alerts...")
    for data in alert_data:
        c.execute('''INSERT INTO destination_alerts 
                    (passenger_name, phone, email, destination_station, train_name)
                    VALUES (?, ?, ?, ?, ?)''', data)
    
    print("✅ Destination alerts added!")
    
    conn.commit()
    conn.close()
    
    print("\n🎉 Sample data added successfully!")
    print("📊 Summary:")
    print(f"   - 15 Crowd Updates")
    print(f"   - 8 Ticket Bookings")
    print(f"   - 4 Destination Alerts")
    print("\n✅ Your database is now populated with realistic Tamil Nadu railway data!")
    print("🌐 Start the app: python app.py")
    print("🔗 Visit: http://localhost:5000")

if __name__ == '__main__':
    add_sample_data()