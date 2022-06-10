import logging
import mimetypes
from django.core.exceptions import ObjectDoesNotExist
from django.core.management.base import BaseCommand, CommandError
from django.db.models import Max
from oral_history.models import ContentFiles, Projects, ProjectItems
from oral_history.scripts.audio_processor import AudioProcessor
from oral_history.scripts.image_processor import ImageProcessor

logger = logging.getLogger(__name__)


def calculate_destination_dir(mime_type, item_ark):
    # https://jira.library.ucla.edu/browse/SYS-808
    # Based on MIME type and project, the destination dir will differ
    # The ark is used to go to DB, get project ID, then get directory
    # based on the mimetype

    try:
        if mime_type in ['image/tif', 'image/tiff']:
            submasters_dir_to_find = 'image_submasters_dir'
        elif mime_type in ['audio/wav', 'audio/x-wav']:
            submasters_dir_to_find = 'audio_submasters_dir'
        elif mime_type in ['something/pdf_related']:
            submasters_dir_to_find = 'lob_submasters_dir'
        elif mime_type in ['something/text_related']:
            submasters_dir_to_find = 'text_submasters_dir'

        # TODO: Refactor this to avoid repeated code
        pfk_value = ProjectItems.objects.filter(
            item_ark=item_ark).first().projectid_fk_id
        submasters_dir = getattr(Projects.objects.get(
            pk=pfk_value), submasters_dir_to_find)

        submaster_dir = str(submasters_dir)
        logger.info(f'{submaster_dir = }')

        submaster_mime = mime_type
        logger.info(f'{submaster_mime = }')

        # This function might be removed completely upon refactor
        # Local environment variables will replace root dir to return
        # Temporarily using "/tmp/" as local placeholder
        submasters_dir = "/tmp/"

        return submasters_dir
    except Exception as ex:
        logger.exception(ex)
        # Re-raise the exception for the view to handle
        raise


def process_media_file(file_name, item_ark, file_group):
    mime_type, encoding = mimetypes.guess_type(file_name)
    logger.info(f'{mime_type = }')
    try:
        mime_type = mime_type.lower()
        dest_dir = calculate_destination_dir(mime_type, item_ark)
        if mime_type in ['image/tif', 'image/tiff']:
            derivative_data = process_tiff(file_name, item_ark, dest_dir)
        elif mime_type in ['audio/wav', 'audio/x-wav']:
            derivative_data = process_wav(file_name, item_ark, dest_dir)
        elif mime_type in ['something/pdf_related']:
            process_pdf(file_name, item_ark, dest_dir)
        elif mime_type in ['something/text_related']:
            process_text(file_name, item_ark, dest_dir)
        else:
            raise CommandError(f'MIME type not recognized for {file_name}')

        update_db(derivative_data, item_ark, file_group)
    except AttributeError as ex:
        if mime_type is None:
            logger.error(f'Invalid {mime_type = }')
            raise CommandError(f'No MIME type identified for {file_name}')
    except Exception as ex:
        logger.exception(ex)
        # Re-raise the exception for the view to handle
        raise


def process_tiff(file_name, item_ark, dest_dir):
    # https://jira.library.ucla.edu/browse/SYS-837
    # TODO:
    # Calculate thumbnail height and width from admin metadata
    resize_height, resize_width = 50, 50

    try:
        dest_file_name = dest_dir + get_new_content_file_name(item_ark, "thumbnail", "jpg")
        logger.info(f'{dest_file_name = }')

        image_processor = ImageProcessor(file_name)
        img_metadata = image_processor.create_thumbnail(dest_file_name, resize_height, resize_width)

        return img_metadata

    except Exception as ex:
        logger.exception(ex)
        raise


def process_wav(file_name, item_ark, dest_dir):

    try:
        dest_file_name = dest_dir + get_new_content_file_name(item_ark, "submaster", "mp3")
        logger.info(f'{dest_file_name = }')

        audio_processor = AudioProcessor(file_name)
        audio_metadata = audio_processor.create_audio_mp3(dest_file_name)

        return audio_metadata

    except Exception as ex:
        logger.exception(ex)
        raise


def process_pdf(file_name, item_ark, dest_dir):
    # https://jira.library.ucla.edu/browse/SYS-831
    pass


def process_text(file_name, item_ark, dest_dir):
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

def get_new_content_file_name(item_ark, file_use, file_extension):
    # Returned file name should be all lowercase and ark slash replaced with dash
    # If no record found for submitted ark, return None

    project_item = get_project_item(item_ark)

    if project_item:
        file_sequence = str(get_next_seq_from_content_files(project_item.divid_pk))

        item_ark = item_ark.replace("/", "-")

        content_file_name = f'{item_ark}-{file_sequence}-{file_use}.{file_extension}'.lower()

        return content_file_name
    
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
