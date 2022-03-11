from django import forms

from .models import Projects

class ProjectsForm(forms.ModelForm):

    class Meta:
        model = Projects
        exclude = ['projectid_pk']