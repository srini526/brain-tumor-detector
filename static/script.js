// static/script.js

document.getElementById('predict-button').addEventListener('click', function() {
    const fileInput = document.getElementById('file-input');
    const resultText = document.getElementById('result-text');

    if (fileInput.files.length === 0) {
        alert("Please select an MRI scan image first.");
        return;
    }

    const file = fileInput.files[0];
    const formData = new FormData();
    formData.append('file', file);

    resultText.textContent = "Analyzing...";
    resultText.style.color = "#333"; // Reset color

    fetch('/predict', {
        method: 'POST',
        body: formData
    })
    .then(response => response.json())
    .then(data => {
        if (data.prediction) {
            resultText.textContent = data.prediction;
            
            // --- NEW: Change color based on the result ---
            if (data.prediction === "Tumor Detected") {
                resultText.style.color = "#d9534f"; // Red for danger
            } else if (data.prediction === "No Tumor Detected") {
                resultText.style.color = "#5cb85c"; // Green for safe
            } else {
                // For "Invalid Input File" or other messages
                resultText.style.color = "#f0ad4e"; // Orange for warning
            }

        } else {
            resultText.textContent = 'Error: ' + data.error;
            resultText.style.color = "#d9534f";
        }
    })
    .catch(error => {
        console.error('Error:', error);
        resultText.textContent = 'An error occurred during prediction.';
        resultText.style.color = "#d9534f";
    });
});