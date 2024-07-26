document.getElementById('login-form').addEventListener('submit', function(event) {
    event.preventDefault();
    
    const username = document.getElementById('username').value;
    const password = document.getElementById('password').value;
    const errorMessage = document.getElementById('error-message');
    
    // Example of valid username and password
    const validUsername = 'psyaj9';
    const validPassword = 'password';
    
    if (username === validUsername && password === validPassword) {
        // Goes to search html is successful
        window.location.href = 'search.html';
    } else {
        // Error message if incorrect
        errorMessage.textContent = 'Incorrect details. Please try again.';
    }
});
