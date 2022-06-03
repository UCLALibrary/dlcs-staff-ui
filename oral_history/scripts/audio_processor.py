#!/usr/bin/env python3

import datetime
import ffmpeg
import logging
import mimetypes
import os
from django.core.management.base import CommandError
from oral_history.models import ContentFiles

logger = logging.getLogger(__name__)

class AudioProcessor():

    AUDIO_CONTENT_TYPE = "Audio"

    def __init__(self, src_file_name):
        self.src_file_name = src_file_name
        logger.info(f'Processing audio: {src_file_name}')

    def populate_content_file_data(self, file_path):
        
        mime_type, encoding = mimetypes.guess_type(file_path)

        img_metadata = ContentFiles()
        img_metadata.mime_type = mime_type
        img_metadata.file_sequence = 0
        img_metadata.file_size = os.path.getsize(file_path)
        img_metadata.create_date = datetime.date.today()
        img_metadata.file_location = file_path
        img_metadata.location_type = 'Submaster'
        img_metadata.content_type = self.AUDIO_CONTENT_TYPE

        return img_metadata
    
    def create_audio_mp3(self, dest_file_name):
        
        logger.info(f"Mp3 generation with source and output files: ('{self.src_file_name}', '{dest_file_name} )")

        try:
            stream = ffmpeg.input(self.src_file_name)
            stream = ffmpeg.output(stream, dest_file_name, acodec='libmp3lame', audio_bitrate='320k', ar=44100, ac=2)
            ffmpeg.run(stream)

            audio_metadata = self.populate_content_file_data(dest_file_name)

            return audio_metadata

        except:
            raise CommandError(f'Error processing file')
        
        logger.info(f'Audio processed: {dest_file_name}')
