import mimetypes
import string
from django.core.management.base import BaseCommand, CommandError
from wand.image import Image

# Global variables for testing -- will be removed going forward
dest_dir = '/tmp/'

def calculate_destination_dir(mime_type, ark):
    # Based on MIME type and project, the destination dir will differ
    # Using temp placeholder for now

    # TODO:
    # Need to use ark to go to DB, get project ID, then get directory
    # based on the mimetype

    return dest_dir

def process_tiff_image(file_name, ark, dest_dir):
    # TODO:
    # Calculate destination filename based on ark and sequence id from DB
    # Using tmp name for place holder

    dest_filename = dest_dir + 'tmp.jpg'
    img = Image(filename=file_name)
    img.save(filename=dest_filename)

def process_wav_image(filename, ark, dest_dir):
    # Placeholder for ffmpeg/audio processing
    pass


class Command(BaseCommand):
    help = 'Django management command to process files'

    def add_arguments(self, parser):
        
        # Required arguments: 
        # -f, --filename : Absolute file path of file to process
        # -a, --ark : The Archival Resource Key of the item to attach the submitted file to

        parser.add_argument('-f','--filename', type=str, required=True, help='The full path of file to process')
        parser.add_argument('-a','--ark', type=str, required=True, help='The ARK of the item to attach file to')


    
    def handle(self, *args, **options):
        filename = options['filename']
        ark = options['ark']

        mime_type, encoding = mimetypes.guess_type(filename)

        # Try/Catch if invalid mime and/or project/ark
        dest_dir = calculate_destination_dir(mime_type, ark)

        # Only process specific MIME types
        if mime_type.casefold() in  ['image/tif', 'image/tiff'] :
            process_tiff_image(filename, ark, dest_dir)

        elif mime_type.casefold() in ['audio/wav', 'audio/x-wav'] :
            process_wav_image(filename, ark, dest_dir)
        
        else :
            raise CommandError('MIME type not recognized for "%s"' % filename)

        # Sanity output
        self.stdout.write('File submitted is %s' % mime_type)
        self.stdout.write('Ark submitted is %s' % ark)
        self.stdout.write('File submitted is %s' % filename)



