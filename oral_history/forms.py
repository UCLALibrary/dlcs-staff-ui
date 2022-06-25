import os
from django import forms
from django.core.cache import cache
from .models import Projects, FileGroups
from .settings import PROJECT_ID

DLCS_FILE_SOURCE = os.getenv('DJANGO_DLCS_FILE_SOURCE')
# Get list of tuples of Oral History Project file groups, using primary key as form value
FILE_GROUPS = [(f.pk, f.description) for f in FileGroups.objects.filter(projectid_fk_id__exact=PROJECT_ID)]

class ProjectsForm(forms.ModelForm):

    class Meta:
        model = Projects
        exclude = ['projectid_pk']


class FileUploadForm(forms.Form):
    file_group = forms.ChoiceField(
        choices=FILE_GROUPS, required=True,)
    # FilePathField (at least) path gets cached automatically by Django at application startup.
    # There's no direct way to make it see changes to the filesystem.
    # Workaround from https://stackoverflow.com/questions/30656653/suffering-stale-choices-for-filepathfield

    _file_name_kw = dict(
        path=DLCS_FILE_SOURCE, 
        recursive=True, 
        allow_files=True, 
        allow_folders=False
    )
    file_name = forms.FilePathField(**_file_name_kw)

    # __init__ is called every time the form is needed.
    # Cache values for 5 seconds (arbitrary); use cache if populated,
    # otherwise start fresh.
    def __init__(self, *args, **kwargs):
        seconds_to_cache = 5
        key = 'file_name-cache-key'
        choices = cache.get(key)
        if not choices:
            field = forms.FilePathField(**self._file_name_kw)
            choices = field.choices
            cache.set(key, choices, seconds_to_cache)

        super().__init__(*args, **kwargs)
        self.base_fields['file_name'].choices = choices
