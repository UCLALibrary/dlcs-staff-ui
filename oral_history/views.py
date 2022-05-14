from django.shortcuts import render
from .forms import FileUploadForm, ProjectsForm
from .models import Projects, ProjectItems
from django.core.management import call_command
from django.contrib import messages
from django.core.management.base import CommandError


def projects_new(request):
    form = ProjectsForm()
    return render(request, 'oral_history/project.html', {'form': form})


def upload_file(request):
    id = request.GET.get('divid_pk')
    query_results = ProjectItems.objects.filter(divid_pk=id)

    if request.method == 'POST':
        form = FileUploadForm(request.POST)
        if form.is_valid():
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
            file_name = request.POST['file_name'][0]
            pfk_value = ProjectItems.objects.filter(
                divid_pk=id).values('projectid_fk')[0]['projectid_fk']

            try:
                call_command('run_script', file_group=file_group, file_name=file_name,
                             item_ark=item_ark)
                # print(file_name)

                path_dir = Projects.objects.filter(
                    projectid_pk=pfk_value).values('image_masters_dir')[0]['image_masters_dir']

                messages.success(
                    request, "The media file was successfully processed")
                messages.success(request, pfk_value)
                messages.success(request, path_dir)

            # CommandErrors is set in the media processing script
            except CommandError as e:
                print(str(e))
                messages.error(
                    request, str(e))
            except ZeroDivisionError as e:
                messages.error(
                    request, "Zero division error: " + str(e))
            except Exception as e:
                messages.error(
                    request, "General error: " + str(e))

        else:
            messages.error(
                request, "Please check the form fields and resubmit")
    else:
        form = FileUploadForm()

    return render(request, 'oral_history/fileupload.html', {'form': form, 'query_results': query_results})


def projects_table(request):
    query_results = ProjectItems.objects.all()
    return render(request, 'oral_history/table.html', {'query_results': query_results})
