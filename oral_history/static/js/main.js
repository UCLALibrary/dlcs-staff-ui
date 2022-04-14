// Custom javascript for the oral history staff ui

// Called when file information form is submitted.
// Captures file name, but does not actually upload the file to server.
function skip_upload(form) {
	// The name of the file selected by user for upload
	var selected_file_name = form.elements.selected_file.value;
	// Copy to a hidden text field for submission
	form.elements.file_name.value = selected_file_name;
	// Clear the name of the file & dir selection fields, which prevents them from being submitted.
	form.elements.selected_file.name = "";
	form.elements.selected_dir.name = "";
	// Handle notification...
	alert(selected_file_name + " will be processed");
}

function list_files(file_list) {
	files = file_list.files;
	radio_list = "";
	for (i = 0; i < files.length; i++) {
		file_path = files[i].webkitRelativePath;
		radio_list += `<p><input type='radio' name='selected_file' value='${file_path}'>${file_path}</p>`;
	}
	// TODO: Pass the target div to this function?
	div = document.getElementById("file_list_div");
	div.innerHTML = radio_list;
	div.removeAttribute("hidden");
}

