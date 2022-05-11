import logging
import mimetypes
from django.core.management.base import BaseCommand, CommandError

logger = logging.getLogger(__name__)

def calculate_destination_dir(mime_type, item_ark):
    # https://jira.library.ucla.edu/browse/SYS-808
    # Based on MIME type and project, the destination dir will differ
    # TODO:
    # Need to use ark to go to DB, get project ID, then get directory
    # based on the mimetype

    # Using temp placeholder for now
    return '/tmp/'

def process_media_file(file_name, item_ark):
    mime_type, encoding = mimetypes.guess_type(file_name)
    logger.info(f'{mime_type = }')
    try:
        mime_type = mime_type.lower()
        dest_dir = calculate_destination_dir(mime_type, item_ark)
        if mime_type in ['image/tif', 'image/tiff']:
            process_tiff(file_name, item_ark, dest_dir)
        elif mime_type in ['audio/wav', 'audio/x-wav']:
            process_wav(file_name, item_ark, dest_dir)
        elif mime_type in ['something/jhove_related']:
            process_jhove(file_name, item_ark, dest_dir)
        else:
            raise CommandError(f'MIME type not recognized for {file_name}')
    except AttributeError as ex:
        if mime_type is None:
            logger.error(f'Invalid {mime_type = }')
            raise CommandError(f'No MIME type identified for {file_name}')
    except Exception as ex:
        logger.exception(ex)
        # Re-raise the exception for the view to handle
        raise

def process_tiff(file_name, item_ark, dest_dir):
    # https://jira.library.ucla.edu/browse/SYS-800
    # TODO:
    # Calculate destination file_name based on ark and sequence id from DB
    # Using tmp name for place holder
    dest_file_name = dest_dir + 'tmp.jpg'
    logger.info(f'{dest_file_name = }')

def process_wav(file_name, item_ark, dest_dir):
    # https://jira.library.ucla.edu/browse/SYS-801
    pass

def process_jhove(file_name, item_ark, dest_dir):
    # https://jira.library.ucla.edu/browse/SYS-802
    pass

def update_db():
    # https://jira.library.ucla.edu/browse/SYS-810
    # Is this done differently based on mime_type / other data?
    pass

class Command(BaseCommand):
    help = 'Django management command to process files'

    def add_arguments(self, parser):
        parser.add_argument('-a','--item_ark', type=str, required=True, help='The ARK of the item to attach file to')
        parser.add_argument('-f','--file_name', type=str, required=True, help='The full path of file to process')
        parser.add_argument('-g','--file_group', type=str, required=True, help='The file group of the file to process')
    
    def handle(self, *args, **options):
        file_group = options['file_group']
        file_name = options['file_name']
        item_ark = options['item_ark']

        # Log arguments, for now
        logger.info(f'\n\n===== Starting new run =====')
        logger.info(f'{file_group = }')
        logger.info(f'{file_name = }')
        logger.info(f'{item_ark = }')

        process_media_file(file_name, item_ark)
