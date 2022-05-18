from django.contrib import admin
from .models import ContentFiles, FileGroups, Projects, ProjectItems


@admin.register(ContentFiles)
class ContentFilesAdmin(admin.ModelAdmin):
    list_display = ('fileid_pk', 'file_groupid_fk', 'divid_fk', 'mime_type', 'file_sequence', 'file_size',
                    'create_date', 'file_location', 'location_type', 'file_use', 'file_name', 'content_type')


@admin.register(FileGroups)
class ProjectGroupsAdmin(admin.ModelAdmin):
    list_display = ('file_groupid_pk', 'projectid_fk',
                    'file_group_title', 'description')


@admin.register(Projects)
class ProjectsAdmin(admin.ModelAdmin):
    list_display = ('projectid_pk', 'project_title')


@admin.register(ProjectItems)
class ProjectItemsAdmin(admin.ModelAdmin):
    list_display = ('divid_pk', 'objectid_fk', 'create_date', 'last_edit_date', 'projectid_fk', 'item_ark', 'sent_to_dpr_flag', 'parent_divid',
                    'item_sequence', 'old_divid', 'old_parent_divid', 'node_title', 'statusid_fk', 'created_by', 'modified_by', 'approved_by')
    search_fields = ('created_by', 'modified_by')
