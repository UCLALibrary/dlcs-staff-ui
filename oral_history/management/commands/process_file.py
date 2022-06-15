import logging
import mimetypes
import os
from django.core.exceptions import ObjectDoesNotExist
from django.core.management.base import BaseCommand, CommandError
from django.db.models import Max
from oral_history.models import ContentFiles, Projects, ProjectItems
from oral_history.scripts.audio_processor import AudioProcessor
from oral_history.scripts.image_processor import ImageProcessor

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
        app_folder = get_app_folder_name(item_ark)
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
            local_root = os.getenv('DJANGO_OH_SUBMASTERSLZ')
    
    elif file_use == "thumbnail":
        local_root = os.getenv('DJANGO_OH_THUMBNAILSLZ')
    
    return local_root
    
def get_app_folder_name(item_ark):
    
    pfk_value = ProjectItems.objects.filter(
        item_ark=item_ark).first().projectid_fk_id
    proj_app_name = getattr(Projects.objects.get(
        pk=pfk_value), "webapp_name")
    
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
        folder_name = "/"
    
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


def process_media_file(file_name, item_ark, file_group):

    try:
        media_type = calculate_media_type(file_name)
        
        if media_type == "image":
            derivative_data = process_tiff(file_name, item_ark)
        
        elif media_type == "audio":
            derivative_data = process_wav(file_name, item_ark)

        elif media_type == "pdf":
            process_pdf(file_name, item_ark)

        elif media_type == "text":
            process_text(file_name, item_ark)

        else:
            raise CommandError(f'Media type not recognized for {file_name}')

        for content_file in derivative_data:
            update_db(content_file, item_ark, file_group)

    except AttributeError as ex:
        if media_type is None:
            logger.error(f'Invalid {media_type = }')
            raise CommandError(f'No media type identified for {file_name}')
    except Exception as ex:
        logger.exception(ex)
        # Re-raise the exception for the view to handle
        raise


def process_tiff(file_name, item_ark):
    # https://jira.library.ucla.edu/browse/SYS-837
    # TODO:
    # Calculate thumbnail height and width from admin metadata
    resize_height, resize_width = 50, 50

    try:
        img_metadata = []
        
        dest_dir = calculate_destination_dir("image", item_ark, "thumbnail")
        cf_name, file_sequence = get_new_content_file_name(item_ark, "thumbnail", "jpg")
        dest_file_name = f"{dest_dir}{cf_name}"
        logger.info(f'{dest_file_name = }')

        image_processor = ImageProcessor(file_name, file_sequence)
        img_metadata.append(image_processor.create_thumbnail(dest_file_name, resize_height, resize_width))

        return img_metadata

    except Exception as ex:
        logger.exception(ex)
        raise


def process_wav(file_name, item_ark):

    try:
        audio_metadata = []

        dest_dir = calculate_destination_dir("audio", item_ark, "submaster")
        cf_name, file_sequence = get_new_content_file_name(item_ark, "submaster", "mp3")
        dest_file_name = f"{dest_dir}{cf_name}"
        logger.info(f'{dest_file_name = }')

        audio_processor = AudioProcessor(file_name, file_sequence)
        audio_metadata.append(audio_processor.create_audio_mp3(dest_file_name))

        return audio_metadata

    except Exception as ex:
        logger.exception(ex)
        raise


def process_pdf(file_name, item_ark):
    # https://jira.library.ucla.edu/browse/SYS-831
    pass


def process_text(file_name, item_ark):
    # https://jira.library.ucla.edu/browse/SYS-832
    pass


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

        content_file_name = f'{item_ark}-{file_sequence}-{file_use}.{file_extension}'.lower()

        return content_file_name, file_sequence
    
    else:
        return None


def update_db(derivative_data, item_ark, file_group):
    # Adds required foreign keys to ContentFiles object, then saves it.
    # file_group already contains a FileGroups primary key, from the calling form.
    project_item = get_project_item(item_ark)
    derivative_data.divid_fk_id = project_item.pk
    derivative_data.file_groupid_fk_id = file_group
    derivative_data.save()

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
