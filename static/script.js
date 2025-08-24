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

    fetch('/predict', {
        method: 'POST',
        body: formData
    })
    .then(response => response.json())
    .then(data => {
        if (data.prediction) {
            resultText.textContent = data.prediction;
            if (data.prediction === "Tumor Detected") {
                resultText.style.color = "#d9534f"; // Red for danger
            } else {
                resultText.style.color = "#5cb85c"; // Green for safe
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