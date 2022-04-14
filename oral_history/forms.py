from django import forms

from .models import Projects

class ProjectsForm(forms.ModelForm):

    class Meta:
        model = Projects
        exclude = ['projectid_pk']

class ExampleFileUploadForm(forms.Form):
    # This displays the file picker for directories, but will not be used
    selected_dir = forms.FileField(
        required=False, 
        widget=forms.FileInput(attrs={'webkitdirectory': '', 'oninput': 'list_files(this);'})
    )
    # This gets the file name (via javascript when the form is submitted)
    file_name = forms.CharField(widget=forms.HiddenInput())
