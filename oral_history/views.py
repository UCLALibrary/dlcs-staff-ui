from django.shortcuts import render
from .forms import ProjectsForm, ExampleFileUploadForm

def projects_new(request):
    form = ProjectsForm()
    return render(request, 'oral_history/project.html', {'form': form})

def upload_test(request):
    if request.method == 'POST':
        form = ExampleFileUploadForm(request.POST)
        # Commented-out code in case we want to really upload files after all.
        # Print statements go to django logs, for QAD dev
        # form = ExampleFileUploadForm(request.POST, request.FILES)
        # selected_file = request.FILES['selected_file']
        # print(f'selected_file => {selected_file}')
        # print(f'Name => {selected_file.name}')
        # print(f'Size => {selected_file.size}')
        # print(f'Type => {selected_file.content_type}')
        print(request.POST['file_name'])
    else:
        form = ExampleFileUploadForm()

    return render(request, 'oral_history/examplefileupload.html', {'form': form})
