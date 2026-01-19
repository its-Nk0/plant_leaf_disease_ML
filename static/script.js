const uploadBox = document.getElementById('uploadBox');
const fileInput = document.getElementById('fileInput');
const predictBtn = document.getElementById('predictBtn');
const resetBtn = document.getElementById('resetBtn');
const resultSection = document.getElementById('resultSection');
const loading = document.getElementById('loading');
const error = document.getElementById('error');
const previewImage = document.getElementById('previewImage');
const diseaseName = document.getElementById('diseaseName');
const confidenceBar = document.getElementById('confidenceBar');
const confidenceValue = document.getElementById('confidenceValue');
const healthStatus = document.getElementById('healthStatus');

let selectedFile = null;

// Upload box click
uploadBox.addEventListener('click', () => fileInput.click());

// File input
fileInput.addEventListener('change', (e) => handleFile(e.target.files[0]));

// Drag and drop
uploadBox.addEventListener('dragover', (e) => {
    e.preventDefault();
    uploadBox.classList.add('dragover');
});

uploadBox.addEventListener('dragleave', () => uploadBox.classList.remove('dragover'));

uploadBox.addEventListener('drop', (e) => {
    e.preventDefault();
    uploadBox.classList.remove('dragover');
    handleFile(e.dataTransfer.files[0]);
});

// Predict button
predictBtn.addEventListener('click', async () => {
    if (!selectedFile) return;
    
    loading.style.display = 'block';
    resultSection.style.display = 'none';
    error.style.display = 'none';
    predictBtn.disabled = true;
    
    const formData = new FormData();
    formData.append('file', selectedFile);
    
    try {
        const response = await fetch('/predict', {
            method: 'POST',
            body: formData
        });
        
        const data = await response.json();
        
        if (data.success) {
            previewImage.src = data.image;
            diseaseName.textContent = data.disease;
            confidenceValue.textContent = `${data.confidence}%`;
            confidenceBar.style.width = `${data.confidence}%`;
            resultSection.style.display = 'block';
        } else {
            showError(data.error || 'Prediction failed');
        }
    } catch (err) {
        showError('Server error: ' + err.message);
    } finally {
        loading.style.display = 'none';
        predictBtn.disabled = false;
    }
});

// Reset button
resetBtn.addEventListener('click', () => {
    selectedFile = null;
    fileInput.value = '';
    resultSection.style.display = 'none';
    error.style.display = 'none';
    predictBtn.disabled = true;
    uploadBox.innerHTML = uploadBox.querySelector('.upload-content').outerHTML;
});

// Handle file
function handleFile(file) {
    if (!file) return;
    
    if (!file.type.startsWith('image/')) {
        showError('Please select an image file');
        return;
    }
    
    if (file.size > 16 * 1024 * 1024) {
        showError('File size must be less than 16MB');
        return;
    }
    
    selectedFile = file;
    predictBtn.disabled = false;
    error.style.display = 'none';
    
    // Show preview
    const reader = new FileReader();
    reader.onload = (e) => {
        const img = document.createElement('img');
        img.src = e.target.result;
        img.style.maxWidth = '200px';
        img.style.borderRadius = '10px';
        img.style.marginTop = '20px';
        uploadBox.appendChild(img);
    };
    reader.readAsDataURL(file);
}

// Show error
function showError(message) {
    error.textContent = '❌ ' + message;
    error.style.display = 'block';
}

// Health check
async function checkHealth() {
    try {
        const response = await fetch('/health');
        const data = await response.json();
        healthStatus.textContent = `✅ Server online`;
        healthStatus.className = 'health-status online';
    } catch {
        healthStatus.textContent = '❌ Server offline';
        healthStatus.className = 'health-status offline';
    }
}

checkHealth();
