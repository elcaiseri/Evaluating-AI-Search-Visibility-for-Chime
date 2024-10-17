document.getElementById('submitBtn').addEventListener('click', function() {
    const queryInput = document.getElementById('query');
    const datasetSelect = document.getElementById('dataset');
    const query = queryInput.value.trim();
    const dataset = datasetSelect.value;
    const answerDiv = document.getElementById('answer');
    const timeDiv = document.getElementById('time');
    const errorDiv = document.getElementById('error');
    const loadingDiv = document.getElementById('loading');

    // Clear previous results
    answerDiv.innerHTML = '';
    timeDiv.innerHTML = '';
    errorDiv.textContent = '';

    if (!query) {
        errorDiv.textContent = 'Please enter a query.';
        return;
    }

    // Show loading indicator
    loadingDiv.style.display = 'block';

    // Send POST request to the backend
    fetch('http://localhost:8000/query', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json',
        },
        body: JSON.stringify({ query: query, dataset: dataset }),
    })
    .then(response => response.json())
    .then(data => {
        loadingDiv.style.display = 'none';
        if (data.detail) {
            errorDiv.textContent = data.detail;
        } else {
            answerDiv.innerHTML = `<h3>AI-Generated Answer</h3><p>${data.answer}</p>`;
            timeDiv.innerHTML = `<hr><p>Response Time: ${(data.time * 1000).toFixed(1)} ms.</p>`;
        }
    })
    .catch(error => {
        loadingDiv.style.display = 'none';
        errorDiv.textContent = 'An error occurred. Please try again.';
        console.error('Error:', error);
    });
});