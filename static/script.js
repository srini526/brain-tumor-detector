// static/script.js
document.addEventListener('DOMContentLoaded', () => {
    const fileInput = document.getElementById('file-input');
    const predictButton = document.getElementById('predict-button');
    // ... (rest of the variable declarations are the same as before)
    const imagePreviewContainer = document.getElementById('image-preview');
    const previewImg = document.getElementById('preview-img');
    const fileNameSpan = document.getElementById('file-name');
    const resultContainer = document.getElementById('result-container');
    const loader = document.getElementById('loader');
    const resultContent = document.getElementById('result-content');
    const resultText = document.getElementById('result-text');

    fileInput.addEventListener('change', () => {
        const file = fileInput.files[0];
        if (file) {
            const reader = new FileReader();
            reader.onload = (e) => { previewImg.src = e.target.result; };
            reader.readAsDataURL(file);
            imagePreviewContainer.classList.remove('hidden');
            fileNameSpan.textContent = file.name;
            predictButton.disabled = false;
            resultContainer.classList.add('hidden');
        }
    });

    predictButton.addEventListener('click', () => {
        const file = fileInput.files[0];
        if (!file) { return; }

        const formData = new FormData();
        formData.append('file', file);

        resultContainer.classList.remove('hidden');
        loader.classList.remove('hidden');
        resultContent.classList.add('hidden');
        predictButton.disabled = true;

        fetch('/predict', { method: 'POST', body: formData })
        .then(response => response.json())
        .then(data => {
            resultText.textContent = data.prediction || data.error;
            resultText.className = ''; // Clear previous classes

            if (data.prediction) {
                // --- UPDATED LOGIC TO APPLY COLORS ---
                if (data.prediction.includes("Tumor Detected")) {
                    resultText.classList.add('result-positive');
                } else if (data.prediction.includes("No Tumor Detected")) {
                    resultText.classList.add('result-negative');
                } else { // For "Invalid Input File"
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
            loader.classList.add('hidden');
            resultContent.classList.remove('hidden');
            predictButton.disabled = false;
        });
    });
});