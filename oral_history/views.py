from django.shortcuts import render
from .forms import ProjectsForm
from .models import ProjectItems


def projects_new(request):
    form = ProjectsForm()
    return render(request, 'oral_history/project.html', {'form': form})


def projects_table(request):
    query_results = ProjectItems.objects.all()
    return render(request, 'oral_history/table.html', {'query_results': query_results})
