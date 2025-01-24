
function scrolldown(event) {
    event.preventDefault(); // Prevent form submission
    window.scrollTo({ top: document.body.scrollHeight, behavior: 'smooth' });
    setTimeout(() => {
        event.target.closest("form").submit(); // Submit the form after scrolling
    }, 1000); // Delay submission to allow scrolling
}

