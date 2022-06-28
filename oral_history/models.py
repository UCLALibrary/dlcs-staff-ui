from django.db import models

# Create your models here.


class DlObjects(models.Model):
    objectid_pk = models.AutoField(primary_key=True, auto_created=True)
    projectid_fk = models.ForeignKey(
        'Projects', models.CASCADE, db_column='projectid_fk')
    object_typeid_fk = models.ForeignKey(
        'DlObjectTypes', models.CASCADE, db_column='object_typeid_fk')
    object_label = models.CharField(max_length=200, blank=True, null=True)
    object_level = models.IntegerField()

    class Meta:
        managed = True
        db_table = 'dl_objects'


class DlObjectTypes(models.Model):
    object_typeid_pk = models.AutoField(primary_key=True, auto_created=True)
    object_type = models.CharField(max_length=25)

    class Meta:
        managed = True
        db_table = 'dl_object_types'


class Projects(models.Model):
    projectid_pk = models.AutoField(primary_key=True, auto_created=True)
    project_title = models.CharField(max_length=200)
    project_manager = models.CharField(max_length=100)
    department = models.CharField(max_length=100, blank=True, null=True)
    working_dir = models.CharField(max_length=500, blank=True, null=True)
    webapp_dir = models.CharField(max_length=500, blank=True, null=True)
    image_masters_dir = models.CharField(max_length=500, blank=True, null=True)
    image_submasters_dir = models.CharField(
        max_length=500, blank=True, null=True)
    audio_masters_dir = models.CharField(max_length=500, blank=True, null=True)
    audio_submasters_dir = models.CharField(
        max_length=500, blank=True, null=True)
    video_masters_dir = models.CharField(max_length=500, blank=True, null=True)
    video_submasters_dir = models.CharField(
        max_length=500, blank=True, null=True)
    text_masters_dir = models.CharField(max_length=500, blank=True, null=True)
    text_submasters_dir = models.CharField(
        max_length=500, blank=True, null=True)
    setup_flag = models.CharField(max_length=3)
    auto_publish_flag = models.CharField(max_length=3)
    lob_masters_dir = models.CharField(max_length=500, blank=True, null=True)
    lob_submasters_dir = models.CharField(
        max_length=500, blank=True, null=True)
    dpr_access_groupid = models.CharField(max_length=30, blank=True, null=True)
    webapp_name = models.CharField(unique=True, max_length=30)
    thumbnail_dir = models.CharField(max_length=500, blank=True, null=True)
    item_ordering_flag = models.CharField(max_length=3, blank=True, null=True)
    website_masters_dir = models.CharField(
        max_length=500, blank=True, null=True)
    oai_flag = models.CharField(max_length=3)

    class Meta:
        managed = True
        db_table = 'projects'
        verbose_name_plural = 'projects'


class ProjectItems(models.Model):
    # TODO: Change this to AutoField for consistency?  Do we need 64 bits for this?
    divid_pk = models.BigAutoField(primary_key=True, auto_created=True)
    objectid_fk = models.ForeignKey(
        'DlObjects', models.CASCADE, db_column='objectid_fk')
    create_date = models.DateField()
    last_edit_date = models.DateField()
    projectid_fk = models.ForeignKey(
        'Projects', models.CASCADE, db_column='projectid_fk')
    item_ark = models.CharField(unique=True, max_length=500)
    sent_to_dpr_flag = models.CharField(max_length=3, blank=True, null=True)
    parent_divid = models.IntegerField(blank=True, null=True)
    item_sequence = models.IntegerField(blank=True, null=True)
    desc_clob = models.TextField(blank=True, null=True)
    old_divid = models.CharField(max_length=100, blank=True, null=True)
    old_parent_divid = models.CharField(max_length=100, blank=True, null=True)
    node_title = models.CharField(max_length=1000, blank=True, null=True)
    statusid_fk = models.ForeignKey(
        'QaStatus', models.CASCADE, db_column='statusid_fk', blank=True, null=True)
    created_by = models.CharField(max_length=30, blank=True, null=True)
    modified_by = models.CharField(max_length=30, blank=True, null=True)
    approved_by = models.CharField(max_length=30, blank=True, null=True)

    class Meta:
        managed = True
        db_table = 'project_items'
        verbose_name_plural = 'project items'


class QaStatus(models.Model):
    statusid_pk = models.AutoField(primary_key=True, auto_created=True)
    status = models.CharField(max_length=40)
    description = models.CharField(max_length=250, blank=True, null=True)

    class Meta:
        managed = True
        db_table = 'qa_status'


class FileGroups(models.Model):
    file_groupid_pk = models.AutoField(primary_key=True, auto_created=True)
    projectid_fk = models.ForeignKey(
        'Projects', models.CASCADE, db_column='projectid_fk')
    file_group_title = models.CharField(max_length=250)
    description = models.CharField(max_length=250, blank=True, null=True)

    class Meta:
        managed = True
        db_table = 'file_groups'
        verbose_name_plural = 'file groups'


class LinkAdminGroups(models.Model):
    admin_linkid_pk = models.AutoField(primary_key=True, auto_created=True)
    admin_groupid_fk = models.ForeignKey(
        'AdminGroups', models.CASCADE, db_column='admin_groupid_fk', blank=True, null=True)
    file_groupid_fk = models.ForeignKey(
        'FileGroups', models.CASCADE, db_column='file_groupid_fk', blank=True, null=True)

    class Meta:
        managed = True
        db_table = 'link_admin_groups'


class AdminGroups(models.Model):
    admin_groupid_pk = models.AutoField(primary_key=True, auto_created=True)
    admin_group_title = models.CharField(max_length=250)
    admin_typeid_fk = models.ForeignKey(
        'AdminTypes', models.CASCADE, db_column='admin_typeid_fk')
    description = models.CharField(max_length=250, blank=True, null=True)

    class Meta:
        managed = True
        db_table = 'admin_groups'


class AdminTypes(models.Model):
    admin_typeid_pk = models.AutoField(primary_key=True, auto_created=True)
    admin_type = models.CharField(max_length=25, blank=True, null=True)

    class Meta:
        managed = True
        db_table = 'admin_types'


class AdminTerms(models.Model):
    admin_termid_pk = models.AutoField(primary_key=True, auto_created=True)
    admin_term = models.CharField(max_length=100)
    control_value_flag = models.CharField(max_length=3, blank=True, null=True)
    qualifier_flag = models.CharField(max_length=3, blank=True, null=True)
    repeat_flag = models.CharField(max_length=3, blank=True, null=True)
    admin_typeid_fk = models.ForeignKey(
        'AdminTypes', models.CASCADE, db_column='admin_typeid_fk')

    class Meta:
        managed = True
        db_table = 'admin_terms'


class AdminQualifiers(models.Model):
    admin_qualifierid_pk = models.AutoField(
        primary_key=True, auto_created=True)
    admin_termid_fk = models.ForeignKey(
        'AdminTerms', models.CASCADE, db_column='admin_termid_fk', blank=True, null=True)
    admin_qualifier = models.CharField(max_length=100, blank=True, null=True)
    qualifier_term_id = models.IntegerField(blank=True, null=True)

    class Meta:
        managed = True
        db_table = 'admin_qualifiers'


class AdminControlValues(models.Model):
    admin_cvid_pk = models.AutoField(primary_key=True, auto_created=True)
    admin_termid_fk = models.ForeignKey(
        'AdminTerms', models.CASCADE, db_column='admin_termid_fk')
    admin_cv = models.CharField(max_length=500)
    admin_cv_source = models.CharField(max_length=200, blank=True, null=True)

    class Meta:
        managed = True
        db_table = 'admin_control_values'


class AdminValues(models.Model):
    admin_valueid_pk = models.AutoField(primary_key=True, auto_created=True)
    admin_termid_fk = models.ForeignKey(
        'AdminTerms', models.CASCADE, db_column='admin_termid_fk')
    # Reduced from 3000 to 2000 for SYS-841 akohler
    admin_value = models.CharField(max_length=2000, blank=True, null=True)
    admin_cvid_fk = models.ForeignKey(
        'AdminControlValues', models.CASCADE, db_column='admin_cvid_fk', blank=True, null=True)
    admin_qualifierid_fk = models.ForeignKey(
        'AdminQualifiers', models.CASCADE, db_column='admin_qualifierid_fk', blank=True, null=True)
    admin_groupid_fk = models.ForeignKey(
        'AdminGroups', models.CASCADE, db_column='admin_groupid_fk')
    admin_profile = models.TextField(blank=True, null=True)

    class Meta:
        managed = True
        db_table = 'admin_values'


class ContentFiles(models.Model):
    fileid_pk = models.AutoField(primary_key=True, auto_created=True)
    file_groupid_fk = models.ForeignKey(
        'FileGroups', models.CASCADE, db_column='file_groupid_fk')
    divid_fk = models.ForeignKey(
        'ProjectItems', models.CASCADE, db_column='divid_fk')
    mime_type = models.CharField(max_length=75, blank=True, null=True)
    file_sequence = models.CharField(max_length=255, blank=True, null=True)
    file_size = models.CharField(max_length=20, blank=True, null=True)
    create_date = models.DateField(blank=True, null=True)
    file_location = models.CharField(max_length=500, blank=True, null=True)
    location_type = models.CharField(max_length=25, blank=True, null=True)
    file_use = models.CharField(max_length=50, blank=True, null=True)
    file_name = models.CharField(max_length=100, blank=True, null=True)
    content_type = models.CharField(max_length=25, blank=True, null=True)

    class Meta:
        managed = True
        db_table = 'content_files'
        verbose_name_plural = 'content files'
