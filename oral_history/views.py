from django.shortcuts import render,redirect,get_object_or_404
from .forms import ProjectsForm
from .models import Projects


def projects_new(request, projectid_pk=None):
    if projectid_pk is None:
        if request.method == "POST":
            form = ProjectsForm(request.POST)
            if form.is_valid():
                project = form.save()
                project.save()
                return redirect('/projects/new', projectid_pk=project.projectid_pk)
        else:
            form = ProjectsForm()
    else:
        obj = get_object_or_404(Projects, projectpk_id=projectid_pk)
        form = ProjectsForm(request.POST or None, instance=obj)
        
    return render(request, 'oral_history/project.html', {'form': form})

def projects_detail(request):
    form = ProjectsForm()
    return render(request, 'oral_history/project.html', {'form': form})