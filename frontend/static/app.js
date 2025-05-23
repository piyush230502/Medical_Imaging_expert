document.addEventListener('DOMContentLoaded', function() {
    const apiKeyForm = document.getElementById('api-key-form');
    const apiKeyInput = document.getElementById('api-key-input');
    const apiKeyMessage = document.getElementById('api-key-message');
    const resetApiKeyBtn = document.getElementById('reset-api-key');
    const uploadForm = document.getElementById('upload-form');
    const imageInput = document.getElementById('image-input');
    const uploadMessage = document.getElementById('upload-message');
    const imagePreview = document.getElementById('image-preview');
    const analysisCard = document.getElementById('analysis-card');
    const analysisResult = document.getElementById('analysis-result');
    const analyzeAnotherBtn = document.getElementById('analyze-another');

    // API Key Save
    apiKeyForm.addEventListener('submit', function(e) {
        e.preventDefault();
        fetch('/configure_api_key', {
            method: 'POST',
            body: new URLSearchParams({ api_key: apiKeyInput.value })
        })
        .then(res => res.json())
        .then(data => {
            apiKeyMessage.textContent = data.message;
            apiKeyMessage.className = data.success ? 'text-success' : 'text-danger';
        })
        .catch(() => {
            apiKeyMessage.textContent = 'Error saving API key.';
            apiKeyMessage.className = 'text-danger';
        });
    });

    // API Key Reset
    resetApiKeyBtn.addEventListener('click', function() {
        fetch('/reset_api_key', { method: 'POST' })
        .then(res => res.json())
        .then(data => {
            apiKeyMessage.textContent = data.message;
            apiKeyMessage.className = 'text-warning';
        });
    });

    // Image Upload & Analysis
    uploadForm.addEventListener('submit', function(e) {
        e.preventDefault();
        uploadMessage.textContent = '';
        imagePreview.innerHTML = '';
        analysisCard.classList.add('d-none');
        const file = imageInput.files[0];
        if (!file) return;
        const formData = new FormData();
        formData.append('file', file);
        fetch('/upload_image', {
            method: 'POST',
            body: formData
        })
        .then(res => res.json())
        .then(data => {
            if (data.success) {
                uploadMessage.textContent = 'Image uploaded successfully!';
                uploadMessage.className = 'text-success';
                imagePreview.innerHTML = `<img src="${data.image_url}" alt="Preview">`;
                analyzeImage(data.image_path);
            } else {
                uploadMessage.textContent = data.error || 'Upload failed.';
                uploadMessage.className = 'text-danger';
            }
        })
        .catch(() => {
            uploadMessage.textContent = 'Error uploading image.';
            uploadMessage.className = 'text-danger';
        });
    });

    function analyzeImage(imagePath) {
        analysisResult.textContent = 'Analyzing image...';
        analysisCard.classList.remove('d-none');
        fetch('/analyze_image', {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify({ image_path: imagePath })
        })
        .then(res => res.json())
        .then(data => {
            if (data.success) {
                analysisResult.textContent = data.analysis;
            } else {
                analysisResult.textContent = data.error || 'Analysis failed.';
            }
        })
        .catch(() => {
            analysisResult.textContent = 'Error during analysis.';
        });
    }

    analyzeAnotherBtn.addEventListener('click', function() {
        analysisCard.classList.add('d-none');
        imagePreview.innerHTML = '';
        uploadForm.reset();
        uploadMessage.textContent = '';
    });
});
