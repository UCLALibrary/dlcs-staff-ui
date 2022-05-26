import os
from django import forms
from .models import Projects, FileGroups

FILE_GROUPS = [(f.pk, f.description) for f in FileGroups.objects.all()]
DLCS_FILE_SOURCE = os.getenv('DJANGO_DLCS_FILE_SOURCE')

class ProjectsForm(forms.ModelForm):

    class Meta:
        model = Projects
        exclude = ['projectid_pk']


class FileUploadForm(forms.Form):
    file_group = forms.ChoiceField(
        choices=FILE_GROUPS, required=True,)
    file_name = forms.FilePathField(
        path=DLCS_FILE_SOURCE, recursive=True, allow_files=True, allow_folders=False,
        )
