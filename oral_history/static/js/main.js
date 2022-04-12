// Custom javascript for the oral history staff ui

// Called when file information form is submitted.
// Captures file name, but does not actually upload the file to server.
function skip_upload(form) {
	// The name of the file selected by user for upload
	var selected_file_name = form.elements.selected_file.files[0].name;
	// Copy to a hidden text field
	form.elements.file_name.value = selected_file_name;
	// Clear the name of the file upload field, which prevents it from being submitted.
	form.elements.selected_file.name = "";
	// Handle notification...
	alert(selected_file_name + " will be processed");
}