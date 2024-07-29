import sqlite3

def create_and_populate_junction_table():
    try:
        # Connect to the patients database
        conn_patients = sqlite3.connect('patients.db')
        cursor_patients = conn_patients.cursor()

        # Create the junction table in the patients database
        cursor_patients.execute('''
        CREATE TABLE IF NOT EXISTS patient_us_scans (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            patient_id INTEGER,
            us_scan_id INTEGER,
            FOREIGN KEY (patient_id) REFERENCES patients(patient_id),
            FOREIGN KEY (us_scan_id) REFERENCES us_scans(us_scan_id)
        )
        ''')
        conn_patients.commit()

        # Assuming we need to link existing patients with their US scans
        # Fetch all patients with their corresponding us_scan_id
        cursor_patients.execute('''
        SELECT patient_id, us_scan_id FROM patients
        ''')
        patient_us_scan_data = cursor_patients.fetchall()

        # Insert the patient and US scan links into the junction table
        cursor_patients.executemany('''
        INSERT INTO patient_us_scans (patient_id, us_scan_id) VALUES (?, ?)
        ''', patient_us_scan_data)
        conn_patients.commit()
        conn_patients.close()

        print("Junction table created and populated successfully.")

    except sqlite3.Error as e:
        print(f"SQLite error: {e}")
    except Exception as e:
        print(f"Unexpected error: {e}")

def main():
    create_and_populate_junction_table()

if __name__ == '__main__':
    main()
