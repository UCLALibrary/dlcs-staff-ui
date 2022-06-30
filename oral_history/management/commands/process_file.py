import logging
import mimetypes
import os
from django.core.exceptions import ObjectDoesNotExist
from django.core.management.base import BaseCommand, CommandError
from django.db.models import F, Max
from oral_history.models import AdminValues, ContentFiles, FileGroups, Projects, ProjectItems
from oral_history.scripts.audio_processor import AudioProcessor
from oral_history.scripts.file_processor import FileProcessor
from oral_history.scripts.image_processor import ImageProcessor
from oral_history.settings import PROJECT_ID
from pathlib import Path

logger = logging.getLogger(__name__)


def calculate_destination_dir(media_type, item_ark, file_use):
    # The proper folder location for a file depends on:
    #
    # mime_type - Type of media
    # item_ark - The 'stub' name of the project
    # file_use - Purpose of the file (master, submaster, thumbnail)

    # Final destination dir formula:
    # Local mount based on location type + 
    # project_app_name (from projects.webapp_name) +
    # mime_type folder name +
    # location_type folder name
    # 
    # Example: ${DJANGO_OH_MASTERSLZ}/oralhistory/audio/masters 

    try: 
        local_root = get_local_root_dir(media_type, file_use)
        app_folder = get_app_folder_name()
        media_folder = get_media_folder_by_mime_type(media_type, file_use)

        logger.info(f"{local_root = }, {app_folder = }, {media_folder =}")
    
        full_dest_dir = f"{local_root}{app_folder}{media_folder}"

        return full_dest_dir 
    
    except Exception as ex:
        logger.exception(ex)
        # Re-raise the exception for the view to handle
        raise

def get_local_root_dir(media_type, file_use):
    
    local_root = None

    if file_use == "master":
        local_root = os.getenv('DJANGO_OH_MASTERSLZ')
    
    elif file_use == "submaster" :
        
        if media_type == "audio":
            local_root = os.getenv('DJANGO_OH_WOWZA')
        
        else:
            local_root = os.getenv('DJANGO_OH_STATIC')
    
    elif file_use == "thumbnail":
        local_root = os.getenv('DJANGO_OH_STATIC')

    if local_root is None:
        raise ValueError(f'local_root is not set: {media_type = }, {file_use = }')
    
    return local_root
    
def get_app_folder_name():
    # App folder name will vary based on environment.
    # May also vary based on project, though for now there's only
    # the oral history project, so use that project_id.
    proj_app_name = getattr(Projects.objects.get(
        pk=PROJECT_ID), "webapp_name")

    # Override for TEST environment only
    if os.getenv('DJANGO_RUN_ENV') == 'test':
        proj_app_name += '-test'
    app_folder_name = f"/{proj_app_name}"
    
    return app_folder_name

def get_folder_by_use(file_use):
    
    file_use_folder = ""

    if file_use == "master":
        file_use_folder = "/masters"
    
    elif file_use == "submaster":
        file_use_folder = "/submasters"

    elif file_use == "thumbnail":
        file_use_folder = "/nails"
    
    return file_use_folder

def get_media_folder_by_mime_type(media_type, file_use):

    folder_name = ""
    file_use_folder = get_folder_by_use(file_use)
        
    if media_type == "image":
        folder_name = ""
    
    elif media_type == "audio":
        folder_name = "/audio"
    
    elif media_type == "text":
        folder_name = "/text"
    
    elif media_type == "pdf":
        folder_name = "/pdf"

    folder_name = f"{folder_name}{file_use_folder}/"

    return folder_name

def calculate_media_type(file_name):

    mime_type, encoding = mimetypes.guess_type(file_name)
    logger.info(f'{mime_type = }')

    mime_type = mime_type.lower()

    
    try:
        if mime_type in ["image/tif", "image/tiff"]:
            media_type = "image"
        elif mime_type in ["audio/wav", "audio/x-wav"]:
            media_type = "audio"
        elif mime_type in ["application/pdf"]:
            media_type = "pdf"
        elif mime_type in ["text/plain", "text/xml", "application/xml"]:
            media_type = "text"
        else:
            raise CommandError(f'MIME type not recognized for {file_name}')
        
        return media_type
    
    except Exception as ex:
        logger.exception(ex)
        # Re-raise the exception for the view to handle
        raise


def get_related_file_group(media_type, target_file_use):
    # Gets the relevant related file group, or returns
    # the master-level file group if no matching target_file_use.
    related_groups = {
        'audio': {'Master': 'MasterAudio', 'Submaster': 'SubMasterAudio'},
        'image': {'Master': 'MasterImage', 'Submaster': 'SubMasterImage', 'Thumbnail': 'ThumbnailImage1'},
        'pdf': {},
        'text': {},
    }

    # Will be None if value not found
    related_title = related_groups.get(media_type).get(target_file_use)
    if related_title:
        # Get the id of the matching file group.  Should be only one but use first() to be sure.
        # Will be None if no match found.
        related_file_group = FileGroups.objects.filter(
            projectid_fk_id__exact=PROJECT_ID,
            file_group_title__startswith=related_title,
            ).values_list('file_groupid_pk', flat=True).first()
    else:
        related_file_group = None

    return related_file_group


def process_media_file(file_name, item_ark, file_group):

    try:
        media_type = calculate_media_type(file_name)
        
        if media_type == "image":
            content_file_data = process_tiff(file_name, item_ark)
        
        elif media_type == "audio":
            content_file_data = process_wav(file_name, item_ark, file_group)

        elif media_type == "pdf":
            content_file_data = process_file(file_name, item_ark, media_type, file_group)

        elif media_type == "text":
            content_file_data = process_file(file_name, item_ark, media_type, file_group)

        else:
            raise CommandError(f'Media type not recognized for {file_name}')

        for content_file in content_file_data:
            update_db(content_file, item_ark)

    except AttributeError as ex:
        if media_type is None:
            logger.error(f'Invalid {media_type = }')
            raise CommandError(f'No media type identified for {file_name}')
    except Exception as ex:
        logger.exception(ex)
        # Re-raise the exception for the view to handle
        raise


def process_tiff(file_name, item_ark):

    # Get thumbnail-related settings
    thumbnail_settings = get_thumbnail_settings()
    # This has other values - see function definition -
    # but for now just grab side size in 'Image Pixels Long Dimension'
    resize_height = resize_width = thumbnail_settings['Image Pixels Long Dimension']

    # Get submaster image related settings
    submaster_img_settings = get_submaster_image_settings()
    submaster_img_resize_height = submaster_img_resize_width = submaster_img_settings['Image Pixels Long Dimension']

    try:
        img_metadata = []
        
        # Thumbnail related operations
        dest_dir = calculate_destination_dir("image", item_ark, "thumbnail")
        cf_name, file_sequence = get_new_content_file_name(item_ark, "thumbnail", ".jpg")
        dest_file_name = f"{dest_dir}{cf_name}"
        logger.info(f'{dest_file_name = }')

        file_group = get_related_file_group("image", "Thumbnail")
        image_processor = ImageProcessor(file_name, file_sequence, file_group)
        img_metadata.append(image_processor.create_thumbnail(dest_file_name, resize_height, resize_width))

        # Submaster image related operations
        dest_dir = calculate_destination_dir("image", item_ark, "submaster")
        cf_name, file_sequence = get_new_content_file_name(item_ark, "submaster", ".jpg", file_sequence)
        dest_file_name = f"{dest_dir}{cf_name}"
        logger.info(f'{dest_file_name = }')
        file_group = get_related_file_group("image", "Submaster")
        image_processor.file_group = file_group
        img_metadata.append(image_processor.create_submaster_img(dest_file_name, submaster_img_resize_height, submaster_img_resize_width))
        
        # Master image related operations
        file_ext = Path(file_name).suffix

        dest_dir = calculate_destination_dir("image", item_ark, "master")
        cf_name, file_sequence = get_new_content_file_name(item_ark, "master", file_ext, file_sequence)
        dest_file_name = f"{dest_dir}{cf_name}"
        logger.info(f'{dest_file_name = }')

        file_group = get_related_file_group("image", "Master")
        file_processor = FileProcessor(file_name, file_sequence, file_group, "Master", "Image")
        img_metadata.append(file_processor.copy_file(dest_file_name))

        return img_metadata

    except Exception as ex:
        logger.exception(ex)
        raise


def process_wav(file_name, item_ark, file_group):

    try:
        audio_metadata = []

        dest_dir = calculate_destination_dir("audio", item_ark, "submaster")
        cf_name, file_sequence = get_new_content_file_name(item_ark, "submaster", ".mp3")
        dest_file_name = f"{dest_dir}{cf_name}"
        logger.info(f'{dest_file_name = }')

        file_group = get_related_file_group("audio", "Submaster")
        audio_processor = AudioProcessor(file_name, file_sequence, file_group, "Submaster")
        audio_metadata.append(audio_processor.create_audio_mp3(dest_file_name))

        file_ext = Path(file_name).suffix

        dest_dir = calculate_destination_dir("audio", item_ark, "master")
        cf_name, file_sequence = get_new_content_file_name(item_ark, "master", file_ext, file_sequence)
        dest_file_name = f"{dest_dir}{cf_name}"
        logger.info(f'{dest_file_name = }')

        file_group = get_related_file_group("audio", "Master")
        file_processor = FileProcessor(file_name, file_sequence, file_group, "Master", "Audio")
        audio_metadata.append(file_processor.copy_file(dest_file_name))

        return audio_metadata

    except Exception as ex:
        logger.exception(ex)
        raise


def process_file(file_name, item_ark, media_type, file_group):
    # For those media types that do not require processing, 2 copies of the file
    # represent the master and submaster records
    file_metadata = []

    file_ext = Path(file_name).suffix
    
    dest_dir = calculate_destination_dir(media_type, item_ark, "submaster")
    cf_name, file_sequence = get_new_content_file_name(item_ark, "submaster", file_ext)
    dest_file_name = f"{dest_dir}{cf_name}"
    file_processor = FileProcessor(file_name, file_sequence, file_group, "Submaster", media_type)
    file_metadata.append(file_processor.copy_file(dest_file_name))


    dest_dir = calculate_destination_dir(media_type, item_ark, "master")
    cf_name, file_sequence = get_new_content_file_name(item_ark, "master", file_ext, file_sequence)
    dest_file_name = f"{dest_dir}{cf_name}"
    file_processor.file_use = "Master"
    file_processor.file_sequence = file_sequence
    file_metadata.append(file_processor.copy_file(dest_file_name))

    return file_metadata


def get_project_item(item_ark):
    # Given an ARK, return the full ProjectItem, or None if there's no match.
    try:
        return ProjectItems.objects.get(item_ark=item_ark)
    except ObjectDoesNotExist:
        return None


def get_content_files_for_project_item(divid):
    # Given a div_id return list of ContentFiles, or empty QuerySet if no match
    return ContentFiles.objects.filter(divid_fk=divid)
  

def get_next_seq_from_content_files(divid):
    # Return the max + 1 sequence for content files associated with a project item (div_id)
    # If no records exist, return 1
    
    cf = get_content_files_for_project_item(divid)
    
    if cf.exists():
        seq_string = cf.aggregate(seq=Max('file_sequence'))['seq']
        return int(seq_string) + 1 if len(seq_string) > 0 else 1
    
    else:
        return 1

def get_new_content_file_name(item_ark, file_use, file_extension, file_seq_override = None):
    # Returned file name should be all lowercase and ark slash replaced with dash
    # If no record found for submitted ark, return None

    project_item = get_project_item(item_ark)

    if project_item:
        if file_seq_override:
            file_sequence = file_seq_override
        else:
            file_sequence = str(get_next_seq_from_content_files(project_item.divid_pk))

        item_ark = item_ark.replace("/", "-")

        content_file_name = f'{item_ark}-{file_sequence}-{file_use}{file_extension}'.lower()
        logger.info(f'{content_file_name = }')

        return content_file_name, file_sequence
    
    else:
        return None


def get_thumbnail_settings():
    return get_image_settings("Image Thumbnail Technical MD")


def get_submaster_image_settings():
    return get_image_settings("Image Submaster Technical MD")


def get_image_settings(admin_group_title):
    # Retrieve default image settings from database based on image admin group submitted
    query_data = AdminValues.objects.filter(
        admin_groupid_fk__admin_group_title__exact=admin_group_title,
        admin_termid_fk__admin_term__in=(
            'Bits Per Sample',
            'Image Pixels Long Dimension',
            'Image Quality',
            'Image Sampling Frequency')
        ).select_related('admin_termid_fk').values(
        'admin_value',
        admin_term=F('admin_termid_fk__admin_term')
        )
    # Convert queryset (list of dictionaries) to single dictionary for easier use.
    # At present this returns the following for thumbnails:
    # {
    #     'Image Sampling Frequency': '72',
    #     'Bits Per Sample': '8',
    #     'Image Quality': '75',
    #     'Image Pixels Long Dimension': '200'
    # }
    return {row['admin_term'] : row['admin_value'] for row in query_data}


def update_db(content_file_data, item_ark):
    # Adds required foreign keys to ContentFiles object, then saves it.
    project_item = get_project_item(item_ark)
    content_file_data.divid_fk_id = project_item.pk
    content_file_data.save()


def get_url_message(content_file_data):
    # Builds HTML containing URL(s) for generated content files
    html = '<ul>'
    for content_file in content_file_data:
        if content_file.file_location.startswith('http'):
            html += f'<li><a href="{content_file.file_location}"">{content_file.file_use}</a></li>'
        else:
            html += f'<li>{content_file.file_use} = {content_file.file_location}</li>'
    html += '</ul>'
    return html


class Command(BaseCommand):
    help = 'Django management command to process files'

    def add_arguments(self, parser):
        parser.add_argument('-a', '--item_ark', type=str, required=True,
                            help='The ARK of the item to attach file to')
        parser.add_argument('-f', '--file_name', type=str,
                            required=True, help='The full path of file to process')
        parser.add_argument('-g', '--file_group', type=str, required=True,
                            help='The file group of the file to process')

    def handle(self, *args, **options):
        file_group = options['file_group']
        file_name = options['file_name']
        item_ark = options['item_ark']

        # Log arguments, for now
        logger.info(f'\n\n===== Starting new run =====')
        logger.info(f'{file_group = }')
        logger.info(f'{file_name = }')
        logger.info(f'{item_ark = }')

        process_media_file(file_name, item_ark, file_group)
