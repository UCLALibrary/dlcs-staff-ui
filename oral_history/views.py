from django.shortcuts import render
from .forms import ProjectsForm

def projects_new(request):
    form = ProjectsForm()
    return render(request, 'oral_history/project.html', {'form': form})