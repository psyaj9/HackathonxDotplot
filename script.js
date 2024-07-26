document.getElementById('search-form').addEventListener('submit', function(event) {
    event.preventDefault();
    
    const patientId = document.getElementById('patient-id').value;
    const errorMessage = document.getElementById('error-message');
    const resultsDiv = document.getElementById('results');
    
    // Example of a validPatientID
    const validPatientId = '12345';
    
    if (patientId === validPatientId) {
        errorMessage.textContent = '';
        
        // Display search result
        resultsDiv.innerHTML = `
            <h2>Search Results</h2>
            <p><strong>Patient ID:</strong> ${patientId}</p>
            <p><strong>Patient Name:</strong> Athikash</p>
        `;
    } else {
        // Display error message if patient ID is incorrect
        errorMessage.textContent = 'Incorrect patient ID. Please try again.';
        
        resultsDiv.innerHTML = '';
    }
});


