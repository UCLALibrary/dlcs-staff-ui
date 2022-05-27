import os
from django import forms
from .models import Projects

FILE_GROUPS = [
    ('PDF', 'UCLA Center for Oral History Research Interview Collection PDF'),
    ('Text Transcript', 'Oral History Text - Transcript'),
    ('Text Index', 'Oral History Text - Index'),
    ('MasterImage1', 'Oral History Image - Master Image'),
    ('Text Introduction', 'Oral History Text - Introduction'),
    ('Text Biography', 'Oral History Text - Biography'),
    ('Text Interview History', 'Oral History Text - Interview History'),
    ('Text Appendix', ' Oral History Text - Appendix'),
    ('PDF Appendix to Interview', ' Appendix to Interview PDF'),
    ('PDF Résumé', ' Narrator’s Résumé PDF'),
    ('PDF Legal Agreement', 'PDF Legal Agreement')
]
GROUP_DEFAULT = 'PDF'
DLCS_FILE_SOURCE = os.getenv('DJANGO_DLCS_FILE_SOURCE')

class ProjectsForm(forms.ModelForm):

    class Meta:
        model = Projects
        exclude = ['projectid_pk']


class FileUploadForm(forms.Form):
    file_group = forms.ChoiceField(
        choices=FILE_GROUPS, initial=GROUP_DEFAULT, required=False,)
    # path set in settings.py
    file_name = forms.FilePathField(
        path=DLCS_FILE_SOURCE, recursive=True, allow_files=True, allow_folders=False,
        )
