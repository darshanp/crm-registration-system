// Wait for DOM to load
document.addEventListener('DOMContentLoaded', () => {
    loadCountryCodes();
    setupProfilePicturePreview();
    setupFormSubmission();
});

// Load country codes from API
async function loadCountryCodes() {
    try {
        const response = await fetch('/api/country-codes');
        const data = await response.json();

        if (data.success) {
            const select = document.getElementById('countryCode');
            data.data.forEach(item => {
                const option = document.createElement('option');
                option.value = item.code;
                option.textContent = `${item.code} (${item.country})`;
                select.appendChild(option);
            });

            // Set default to +1 (US/Canada)
            select.value = '+1';
        }
    } catch (error) {
        console.error('Failed to load country codes:', error);
    }
}

// Profile picture preview
function setupProfilePicturePreview() {
    const fileInput = document.getElementById('profilePicture');
    const preview = document.getElementById('profilePreview');

    preview.addEventListener('click', () => {
        fileInput.click();
    });

    fileInput.addEventListener('change', (e) => {
        const file = e.target.files[0];
        if (file) {
            // Validate file type
            const validTypes = ['image/jpeg', 'image/png', 'image/gif'];
            if (!validTypes.includes(file.type)) {
                showError('Invalid file type. Please upload a JPEG, PNG, or GIF image.');
                fileInput.value = '';
                return;
            }

            // Validate file size (5MB)
            if (file.size > 5 * 1024 * 1024) {
                showError('File too large. Maximum size is 5MB.');
                fileInput.value = '';
                return;
            }

            // Show preview
            const reader = new FileReader();
            reader.onload = (e) => {
                preview.innerHTML = `<img src="${e.target.result}" alt="Profile preview">`;
            };
            reader.readAsDataURL(file);
        }
    });
}

// Form submission
function setupFormSubmission() {
    const form = document.getElementById('registrationForm');

    form.addEventListener('submit', async (e) => {
        e.preventDefault();

        // Clear previous messages
        hideMessages();

        // Validate form
        if (!validateForm()) {
            return;
        }

        // Show loading state
        setLoadingState(true);

        try {
            // Create FormData
            const formData = new FormData(form);

            // Send to API
            const response = await fetch('/api/register', {
                method: 'POST',
                body: formData,
            });

            const data = await response.json();

            if (response.ok && data.success) {
                showSuccess(data.message);
                form.reset();
                document.getElementById('profilePreview').innerHTML = `
                    <span class="upload-icon">📷</span>
                    <span class="upload-text">Click to upload</span>
                `;
            } else {
                showError(data.detail || 'Registration failed. Please try again.');
            }
        } catch (error) {
            showError('Network error. Please check your connection and try again.');
            console.error('Registration error:', error);
        } finally {
            setLoadingState(false);
        }
    });
}

// Validate form
function validateForm() {
    const name = document.getElementById('name').value.trim();
    const email = document.getElementById('email').value.trim();
    const dob = document.getElementById('dateOfBirth').value;
    const countryCode = document.getElementById('countryCode').value;
    const phone = document.getElementById('phoneNumber').value.trim();

    if (!name || name.length < 2) {
        showError('Please enter a valid name (at least 2 characters).');
        return false;
    }

    if (!email || !isValidEmail(email)) {
        showError('Please enter a valid email address.');
        return false;
    }

    if (!dob) {
        showError('Please enter your date of birth.');
        return false;
    }

    // Check age (must be 18+)
    const age = calculateAge(new Date(dob));
    if (age < 18) {
        showError('You must be at least 18 years old to register.');
        return false;
    }

    if (!countryCode) {
        showError('Please select a country code.');
        return false;
    }

    if (!phone || !/^\d{7,15}$/.test(phone)) {
        showError('Please enter a valid phone number (7-15 digits, no spaces).');
        return false;
    }

    return true;
}

// Utility functions
function isValidEmail(email) {
    return /^[^\s@]+@[^\s@]+\.[^\s@]+$/.test(email);
}

function calculateAge(birthdate) {
    const today = new Date();
    let age = today.getFullYear() - birthdate.getFullYear();
    const monthDiff = today.getMonth() - birthdate.getMonth();
    if (monthDiff < 0 || (monthDiff === 0 && today.getDate() < birthdate.getDate())) {
        age--;
    }
    return age;
}

function setLoadingState(loading) {
    const btn = document.getElementById('submitBtn');
    const btnText = document.getElementById('btnText');
    const btnLoader = document.getElementById('btnLoader');

    if (loading) {
        btn.disabled = true;
        btnText.style.display = 'none';
        btnLoader.style.display = 'block';
    } else {
        btn.disabled = false;
        btnText.style.display = 'block';
        btnLoader.style.display = 'none';
    }
}

function showSuccess(message) {
    const successDiv = document.getElementById('successMessage');
    successDiv.textContent = message;
    successDiv.style.display = 'block';
    successDiv.scrollIntoView({ behavior: 'smooth', block: 'nearest' });
}

function showError(message) {
    const errorDiv = document.getElementById('errorMessage');
    errorDiv.textContent = message;
    errorDiv.style.display = 'block';
    errorDiv.scrollIntoView({ behavior: 'smooth', block: 'nearest' });
}

function hideMessages() {
    document.getElementById('successMessage').style.display = 'none';
    document.getElementById('errorMessage').style.display = 'none';
}
