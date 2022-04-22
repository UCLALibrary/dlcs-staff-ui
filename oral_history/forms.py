from django import forms
from .models import Projects

FILE_GROUPS = [('PDF', 'UCLA Center for Oral History Research Interview Collection PDF'), ('Text Transcript', 'Oral History Text - Transcript'), ('Text Index', 'Oral History Text - Index'), ('MasterImage1', 'Oral History Image - Master Image'), ('Text Introduction', 'Oral History Text - Introduction'), ('Text Biography',
                                                                                                                                                                                                                                                                                                                 'Oral History Text - Biography'), ('Text Interview History', 'Oral History Text - Interview History'), ('Text Appendix', ' Oral History Text - Appendix'), ('PDF Appendix to Interview', ' Appendix to Interview PDF'), ('PDF Résumé', ' Narrator’s Résumé PDF'), ('PDF Legal Agreement', 'PDF Legal Agreement')]
GROUP_DEFAULT = 'PDF'


class ProjectsForm(forms.ModelForm):

    class Meta:
        model = Projects
        exclude = ['projectid_pk']


class FileUploadForm(forms.Form):
    file_group = forms.ChoiceField(
        choices=FILE_GROUPS, initial=GROUP_DEFAULT, required=False,)
    # This displays the file picker for directories, but will not be used
    selected_dir = forms.FileField(
        required=False,
        widget=forms.FileInput(
            attrs={'webkitdirectory': '', 'oninput': 'list_files(this);'})
    )
    # This gets the file name (via javascript when the form is submitted)
    file_name = forms.CharField(widget=forms.HiddenInput())
