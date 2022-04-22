from django.shortcuts import render
from .forms import FileUploadForm, ProjectsForm
from .models import ProjectItems
from django.core.management import call_command


def projects_new(request):
    form = ProjectsForm()
    return render(request, 'oral_history/project.html', {'form': form})


def upload_file(request):
    id = request.GET.get('divid_pk')
    query_results = ProjectItems.objects.filter(divid_pk=id)

    if request.method == 'POST':
        form = FileUploadForm(request.POST)
        # Commented-out code in case we want to really upload files after all.
        # Print statements go to django logs, for QAD dev
        # form = FileUploadForm(request.POST, request.FILES)
        # selected_file = request.FILES['selected_file']
        # print(f'selected_file => {selected_file}')
        # print(f'Name => {selected_file.name}')
        # print(f'Size => {selected_file.size}')
        # print(f'Type => {selected_file.content_type}')
        # print(f'File Group => {selected_file.name}')
        # print(request.POST.get('file_group'))
        file_group = request.POST.get('file_group')
        item_ark = query_results[0].item_ark
        file_name = request.POST['file_name']
        call_command('run_script', file_group=file_group, file_name=file_name,
                     item_ark=item_ark)
        # print(file_name)
    else:
        form = FileUploadForm()

    return render(request, 'oral_history/fileupload.html', {'form': form, 'query_results': query_results})


def projects_table(request):
    query_results = ProjectItems.objects.all()
    return render(request, 'oral_history/table.html', {'query_results': query_results})
