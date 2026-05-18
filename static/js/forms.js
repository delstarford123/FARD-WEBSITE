/**
 * FARD Form Handling and Validation
 */

document.addEventListener('DOMContentLoaded', () => {
    const forms = ['volunteerForm', 'partnerForm', 'farmerForm'];

    forms.forEach(formId => {
        const form = document.getElementById(formId);
        if (form) {
            form.addEventListener('submit', (e) => {
                e.preventDefault();
                handleFormSubmit(form);
            });
        }
    });
});

/**
 * Handles form submission with visual feedback
 * @param {HTMLFormElement} form 
 */
function handleFormSubmit(form) {
    const feedback = document.getElementById('formFeedback');
    const submitBtn = form.querySelector('button[type="submit"]');
    
    // Simulate loading
    submitBtn.disabled = true;
    submitBtn.innerText = 'Submitting...';
    
    // In a real app, you would use fetch() here
    setTimeout(() => {
        feedback.classList.remove('hidden');
        feedback.classList.add('success');
        feedback.innerText = 'Thank you! Your submission has been received. Our team will contact you soon.';
        
        form.reset();
        submitBtn.disabled = false;
        submitBtn.innerText = 'Submitted Successfully';
        
        // Hide feedback after 5 seconds
        setTimeout(() => {
            feedback.classList.add('hidden');
            feedback.classList.remove('success');
            submitBtn.innerText = 'Submit Another';
        }, 5000);
        
    }, 1500);
}

// Basic field validation could be added here
