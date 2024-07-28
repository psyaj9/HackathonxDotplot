import sqlite3

# Define the path to your SQLite database file
db_path = 'patients.db'

# Connect to the SQLite database (it will be created if it doesn't exist)
conn = sqlite3.connect(db_path)
cursor = conn.cursor()

# Create the 'patients' table with the appropriate schema
cursor.execute('''
CREATE TABLE IF NOT EXISTS patients (
    patient_id INTEGER PRIMARY KEY,
    patient_name TEXT,
    age INTEGER,
    height_cm INTEGER,
    weight_kg INTEGER,
    history_of_breast_cancer TEXT,
    us_scan_id TEXT
)
''')

# Commit the changes and close the connection
conn.commit()
conn.close()

print("Database and table created successfully.")

import pandas as pd
import sqlite3
import os

# Define the path to your CSV file
csv_file = 'Patients.csv'

# Print the current working directory for debugging
print(f"Current Working Directory: {os.getcwd()}")

# Check if the file exists
if not os.path.isfile(csv_file):
    raise FileNotFoundError(f"The file {csv_file} does not exist in the current directory.")

# Read the CSV file into a DataFrame
df = pd.read_csv(csv_file)

# Display the content of the DataFrame (optional)
print("CSV Data Loaded:")
print(df.head())

# Connect to SQLite database
conn = sqlite3.connect('patients.db')
cursor = conn.cursor()

# Insert data from DataFrame into the database
for index, row in df.iterrows():
    cursor.execute('''
    INSERT INTO patients (
        patient_id, patient_name, age, height_cm, weight_kg, history_of_breast_cancer, us_scan_id
    ) VALUES (?, ?, ?, ?, ?, ?, ?)
    ''', (
        row['Patient ID'], row['Patient Name'], row['Age'], row['Height (cm)'],
        row['Weight (kg)'], row['History of breast cancer'], row['US scan ID']
    ))

# Commit changes and close the connection
conn.commit()
conn.close()

print("Data inserted into the database successfully.")
