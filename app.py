from flask import Flask, request, jsonify
from flask_cors import CORS
import sqlite3

app = Flask(__name__)
CORS(app)  # Enable CORS for all routes

def get_patient_from_db(patient_id):
    connection = sqlite3.connect('patients.db')
    cursor = connection.cursor()
    cursor.execute("""
        SELECT patient_id, patient_name, age, height_cm, weight_kg, history_of_breast_cancer, us_scan_id 
        FROM patients 
        WHERE patient_id=?
    """, (patient_id,))
    patient = cursor.fetchone()
    connection.close()
    return patient

@app.route('/search', methods=['POST'])
def search_patient():
    data = request.get_json()
    patient_id = data.get('patientId')
    
    if not patient_id:
        return jsonify({'valid': False, 'error': 'Patient ID is required.'}), 400
    
    patient = get_patient_from_db(patient_id)
    
    if patient:
        return jsonify({
            'valid': True, 
            'patient': {
                'patient_id': patient[0],
                'patient_name': patient[1],
                'age': patient[2],
                'height_cm': patient[3],
                'weight_kg': patient[4],
                'history_of_breast_cancer': patient[5],
                'us_scan_id': patient[6]
            }
        })
    else:
        return jsonify({'valid': False, 'error': 'Patient not found.'})

if __name__ == '__main__':
    app.run(debug=True)




