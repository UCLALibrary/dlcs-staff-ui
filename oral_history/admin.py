from django.contrib import admin
from .models import ProjectItems

# create page to display units


@admin.register(ProjectItems)
class ProjectItemsAdmin(admin.ModelAdmin):
    list_display = ('divid_pk', 'objectid_fk', 'create_date', 'last_edit_date', 'projectid_fk', 'item_ark', 'sent_to_dpr_flag', 'parent_divid',
                    'item_sequence', 'old_divid', 'old_parent_divid', 'node_title', 'statusid_fk', 'created_by', 'modified_by', 'approved_by')
    search_fields = ('created_by', 'modified_by')
