// static/script.js

document.addEventListener('DOMContentLoaded', () => {
    const fileInput = document.getElementById('file-input');
    const predictButton = document.getElementById('predict-button');
    const imagePreviewContainer = document.getElementById('image-preview');
    const previewImg = document.getElementById('preview-img');
    const fileNameSpan = document.getElementById('file-name');
    const resultContainer = document.getElementById('result-container');
    const loader = document.getElementById('loader');
    const resultContent = document.getElementById('result-content');
    const resultText = document.getElementById('result-text');

    // Handle file selection
    fileInput.addEventListener('change', () => {
        const file = fileInput.files[0];
        if (file) {
            // Use FileReader to display the image preview
            const reader = new FileReader();
            reader.onload = (e) => {
                previewImg.src = e.target.result;
            };
            reader.readAsDataURL(file);

            // Show the preview container and file name
            imagePreviewContainer.classList.remove('hidden');
            fileNameSpan.textContent = file.name;
            
            // Enable the predict button
            predictButton.disabled = false;
            resultContainer.classList.add('hidden'); // Hide previous result
        }
    });

    // Handle prediction button click
    predictButton.addEventListener('click', () => {
        const file = fileInput.files[0];
        if (!file) {
            alert("Please select an image first.");
            return;
        }

        const formData = new FormData();
        formData.append('file', file);

        // Show loader and result container, hide result text
        resultContainer.classList.remove('hidden');
        loader.classList.remove('hidden');
        resultContent.classList.add('hidden');
        predictButton.disabled = true;

        fetch('/predict', {
            method: 'POST',
            body: formData
        })
        .then(response => response.json())
        .then(data => {
            // Update result text and apply color class
            resultText.textContent = data.prediction || data.error;
            resultText.className = ''; // Clear previous classes

            if (data.prediction) {
                if (data.prediction.includes("Tumor Detected")) {
                    resultText.classList.add('result-positive');
                } else if (data.prediction.includes("No Tumor Detected")) {
                    resultText.classList.add('result-negative');
                } else {
                    resultText.classList.add('result-warning');
                }
            } else {
                resultText.classList.add('result-warning');
            }
        })
        .catch(error => {
            console.error('Error:', error);
            resultText.textContent = 'An error occurred during prediction.';
            resultText.className = 'result-warning';
        })
        .finally(() => {
            // Hide loader and show the result content
            loader.classList.add('hidden');
            resultContent.classList.remove('hidden');
            predictButton.disabled = false;
        });
    });
});