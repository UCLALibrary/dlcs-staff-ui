import logging
import mimetypes
from django.core.management.base import BaseCommand, CommandError

logger = logging.getLogger(__name__)

def calculate_destination_dir(mime_type, ark):
    # https://jira.library.ucla.edu/browse/SYS-808
    # Based on MIME type and project, the destination dir will differ
    # TODO:
    # Need to use ark to go to DB, get project ID, then get directory
    # based on the mimetype

    # Using temp placeholder for now
    return '/tmp/'

def process_media_file(filename, ark):
    mime_type, encoding = mimetypes.guess_type(filename)
    logger.info(f'{mime_type = }')
    # Or exception handling?
    if mime_type is not None:
        mime_type = mime_type.lower()
        dest_dir = calculate_destination_dir(mime_type, ark)
        if mime_type in ['image/tif', 'image/tiff']:
            process_tiff(filename, ark, dest_dir)
        elif mime_type in ['audio/wav', 'audio/x-wav']:
            process_wav(filename, ark, dest_dir)
        else:
            raise CommandError(f'MIME type not recognized for {filename}')
    else:
        raise CommandError(f'MIME type not recognized for {filename}')

def process_tiff(filename, ark, dest_dir):
    # https://jira.library.ucla.edu/browse/SYS-800
    # TODO:
    # Calculate destination filename based on ark and sequence id from DB
    # Using tmp name for place holder
    dest_filename = dest_dir + 'tmp.jpg'
    logger.info(f'{dest_filename = }')

def process_wav(filename, ark, dest_dir):
    # https://jira.library.ucla.edu/browse/SYS-801
    pass

def process_jhove(filename, ark, dest_dir):
    # https://jira.library.ucla.edu/browse/SYS-802
    pass

def update_db():
    # https://jira.library.ucla.edu/browse/SYS-810
    # Is this done differently based on mime_type / other data?
    pass

class Command(BaseCommand):
    help = 'Django management command to process files'

    def add_arguments(self, parser):
        parser.add_argument('-f','--filename', type=str, required=True, help='The full path of file to process')
        parser.add_argument('-a','--ark', type=str, required=True, help='The ARK of the item to attach file to')
    
    def handle(self, *args, **options):
        filename = options['filename']
        ark = options['ark']
        
        # Log arguments, for now
        logger.info(f'\n\n===== Starting new run =====')
        logger.info(f'{filename = }')
        logger.info(f'{ark = }')

        process_media_file(filename, ark)
