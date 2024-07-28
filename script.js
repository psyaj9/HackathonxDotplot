document.getElementById('search-form').addEventListener('submit', function(event) {
    event.preventDefault();
    
    const patientId = document.getElementById('patient-id').value;
    const errorMessage = document.getElementById('error-message');
    const resultsDiv = document.getElementById('results');
    
    fetch('http://127.0.0.1:5000/search', {  // Ensure this matches your Flask server URL and endpoint
        method: 'POST',
        headers: {
            'Content-Type': 'application/json'
        },
        body: JSON.stringify({ patientId })
    })
    .then(response => response.json())
    .then(data => {
        if (data.valid) {
            errorMessage.textContent = '';
            resultsDiv.innerHTML = `
                <h2>Search Results</h2>
                <p><strong>Patient ID:</strong> ${data.patient.patient_id}</p>
                <p><strong>Patient Name:</strong> ${data.patient.patient_name}</p>
                <p><strong>Age:</strong> ${data.patient.age}</p>
                <p><strong>Height:</strong> ${data.patient.height_cm}</p>
                <p><strong>Weight:</strong> ${data.patient.weight_kg}</p>
                <p><strong>History of breast cancer:</strong> ${data.patient.history_of_breast_cancer}</p>
                <p><strong>US scan ID:</strong> ${data.patient.us_scan_id}</p>
            `;
        } else {
            errorMessage.textContent = data.error || 'Incorrect patient ID. Please try again.';
            resultsDiv.innerHTML = '';
        }
    })
    .catch(error => {
        errorMessage.textContent = 'An error occurred. Please try again later.';
        resultsDiv.innerHTML = '';
        console.error('Error:', error);
    });
});







