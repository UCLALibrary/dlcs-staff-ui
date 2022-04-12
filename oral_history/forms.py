from django import forms

from .models import Projects

class ProjectsForm(forms.ModelForm):

    class Meta:
        model = Projects
        exclude = ['projectid_pk']

class ExampleFileUploadForm(forms.Form):
    # This displays the file picker, but will not be used
    selected_file = forms.FileField(required=False)
    # This gets the file name (via javascript when the form is submitted)
    file_name = forms.CharField(widget=forms.HiddenInput())
