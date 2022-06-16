import os
from django import forms
from .models import Projects, FileGroups

DLCS_FILE_SOURCE = os.getenv('DJANGO_DLCS_FILE_SOURCE')
# Get list of tuples of Oral History Project file groups, using primary key as form value
FILE_GROUPS = [(f.pk, f.description) for f in FileGroups.objects.filter(projectid_fk_id__exact=80)]

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
