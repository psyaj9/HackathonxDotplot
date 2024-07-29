import sqlite3
import pandas as pd

# Load the CSV file
file_path = 'US_scans.csv'  # Update with your file path
df = pd.read_csv(file_path)

# Connect to the SQLite database (or create it if it doesn't exist)
conn = sqlite3.connect('us_scans.db')
cursor = conn.cursor()

# Create the table
cursor.execute('''
CREATE TABLE IF NOT EXISTS us_scans (
    us_scan_id INTEGER PRIMARY KEY,
    coordinates TEXT,
    scan_date TEXT,
    diagnosis TEXT
)
''')

# Insert data into the table
for index, row in df.iterrows():
    cursor.execute('''
    INSERT INTO us_scans (us_scan_id, coordinates, scan_date, diagnosis)
    VALUES (?, ?, ?, ?)
    ''', (row['US scan ID'], row['Coordinates'], row['Scan Date'], row['Diagnosis']))

# Commit the transaction and close the connection
conn.commit()
conn.close()

