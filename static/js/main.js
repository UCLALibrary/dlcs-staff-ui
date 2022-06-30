// Custom javascript for the oral history staff ui

// Disable file upload submit button once clicked.
// The button is restored to normal once Django completes processing and re-renders the form.
function disable_upload_button(form) {
	btn = form.elements.upload_button;
	btn.textContent = "Please wait...";
	btn.disabled = true;
}