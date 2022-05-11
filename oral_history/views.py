from django.shortcuts import render
from .forms import FileUploadForm, ProjectsForm
from .models import ProjectItems
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
            file_group = form.cleaned_data['file_group']
            file_name = form.cleaned_data['file_name']
            item_ark = query_results[0].item_ark

            try:
                call_command('process_file', file_group=file_group, file_name=file_name,
                             item_ark=item_ark)
                messages.success(
                    request, "The media file was successfully processed")

            # Errors from process_file, called above
            # TODO: Are there more specific errors to be caught?
            except CommandError as e:
                print(str(e))
                messages.error(
                    request, str(e))
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
