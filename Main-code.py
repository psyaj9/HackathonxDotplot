import sqlite3
import os
from flask import Flask, request, jsonify, send_from_directory, abort


app = Flask(__name__)

base_dir = os.path.dirname(os.path.abspath(__file__))
folder_path = os.path.join(base_dir, 'US scans')
conn = sqlite3.connect('scanID.db')
cursor = conn.cursor()
for filename in os.listdir(folder_path):
    if filename.endswith('.png') or filename.endswith('.jpg') or filename.endswith('.jpeg'):
        scan_id = os.path.splitext(filename)[0]
        image_path = os.path.join(folder_path, filename)
        try:
            cursor.execute('''
            UPDATE scanID
            SET image_path = ?
            WHERE US_scan_ID = ?
            ''', (image_path, scan_id))
            conn.commit()
        except sqlite3.Error as e:
                print(f"An error occurred while updating scan ID {scan_id}: {e}")
conn.close()
@app.route('/patient/<patient_id>', methods = ['GET'])
def api_get_patient_info(patient_id):
    conn = sqlite3.connect('patients.db')
    cursor = conn.cursor()
    try:
        # Prepare the query
        query = 'SELECT * FROM patients WHERE patient_id = ?'
        # Execute the query
        cursor.execute(query, (patient_id,))
        # Fetch the result
        result = cursor.fetchone()
        if result:
            patient_info = {
                "Patient ID": result[0],
                "Patient Name": result[1],
                "Age": result[2],
                "Height (cm)": result[3],
                "Weight (kg)": result[4],
                "History of Breast Cancer": result[5],
                "US Scan ID": result[6]
            }
            return jsonify(patient_info)
        else:
            return jsonify({"error": "Patient not found"}), 404
    except sqlite3.Error as e:
        return jsonify({"error": str(e)}), 500
    finally:
        conn.close()

@app.route('/', methods=['GET','POST'])
def login():
    username = request.form['username']
    password = request.form['password']

    conn = sqlite3.connect('users.db')  # Connect to your user database
    cursor = conn.cursor()

    try:
        query = 'SELECT * FROM users WHERE username = ? AND password = ?'
        cursor.execute(query, (username, password))
        user = cursor.fetchone()

        if user:
            return redirect(url_for('dashboard'))  # Redirect to a dashboard or another page
        else:
            return render_template('login.html', error_message='Invalid username or password')
    except sqlite3.Error as e:
        return render_template('login.html', error_message=f'An error occurred: {e}')
    finally:
        conn.close()

@app.route('/scan/<scan_id>', methods=['GET'])
def get_scan_info(scan_id):
    """Retrieve scan information based on scan ID."""
    conn1 = sqlite3.connect('scanID.db')
    cursor1 = conn1.cursor()
    conn2 = sqlite3.connect('patients.db')
    cursor2 = conn2.cursor()

    try:
        # Prepare the query
        query = 'SELECT * FROM scanID WHERE US_scan_ID = ?'
        cursor1.execute(query, (scan_id,))
        resultScan = cursor1.fetchone()

        query = '''
            SELECT * FROM patients
            WHERE ' ' || US_scan_ID || ' ' LIKE ?;
            '''
        cursor2.execute(query, (f'% {scan_id} %',))
        resultPatient = cursor2.fetchone()
        if resultScan and resultPatient:
            scan_info = {
                "Patient Name": resultPatient[1],
                "Patient ID": resultPatient[0],
                "Scan ID": resultPatient[6],
                "Coordinates": resultScan[1],
                "Scan Date": resultScan[2],
                "Diagnosis": resultScan[3],
                "Image Path": resultScan[4]
            }
        else:
            return jsonify({"error": "Scan not found"}), 404

    except sqlite3.Error as e:
        return jsonify({"error": str(e)}), 500
    finally:
        conn1.close()
        conn2.close()

@app.route('/images/<filename>', methods=['GET'])
def serve_image(filename):
    try:
        return send_from_directory(folder_path, filename)
    except FileNotFoundError:
        abort(404)

@app.route('/')
def home():
    return "Welcome to the Home Page!"

if __name__ == "__main__":
    app.run(debug=True)
