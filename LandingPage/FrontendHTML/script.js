// Function to submit data to the API
function submitData(firstName, phoneNumber) {
    fetch('https://i1zt35df9j.execute-api.us-east-1.amazonaws.com/Prod/submit/', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json',
        },
        body: JSON.stringify({
            first_name: firstName,
            phone: phoneNumber
        }),
    })
    .then(response => response.json())
    .then(data => {
        console.log('Success:', data);
        alert('Thank you for joining Sweet Spots! We will be in touch.');
    })
    .catch((error) => {
        console.error('Error:', error);
        alert('An error occurred. Please try again later.');
    });
}

// Event listener for the top form submission
document.getElementById('signupFormTop').addEventListener('submit', function(event) {
    event.preventDefault();
    const firstName = event.target.first_name.value;
    const phoneNumber = event.target.phone.value;
    submitData(firstName, phoneNumber);
});

// Event listener for the bottom form submission
document.getElementById('signupFormBottom').addEventListener('submit', function(event) {
    event.preventDefault();
    const firstName = event.target.first_name.value;
    const phoneNumber = event.target.phone.value;
    submitData(firstName, phoneNumber);
});
