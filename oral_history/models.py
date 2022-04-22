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


class ProjectItems(models.Model):
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


class QaStatus(models.Model):
    statusid_pk = models.AutoField(primary_key=True, auto_created=True)
    status = models.CharField(max_length=40)
    description = models.CharField(max_length=250, blank=True, null=True)

    class Meta:
        managed = True
        db_table = 'qa_status'
