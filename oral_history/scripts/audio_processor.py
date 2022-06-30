#!/usr/bin/env python3

import datetime
import ffmpeg
import logging
import mimetypes
import os
from django.core.management.base import CommandError
from oral_history.models import ContentFiles
from pathlib import Path

logger = logging.getLogger(__name__)

class AudioProcessor():

    AUDIO_CONTENT_TYPE = "Audio"

    def __init__(self, src_file_name, file_sequence, file_group, file_use):
        self.src_file_name = src_file_name
        self.file_sequence = file_sequence
        self.file_group = file_group
        self.file_use = file_use

        logger.info(f'Processing audio: {src_file_name}')

    def populate_content_file_data(self, file_path):
        
        mime_type, encoding = mimetypes.guess_type(file_path)

        content_metadata = ContentFiles()
        
        content_metadata.content_type = self.AUDIO_CONTENT_TYPE
        content_metadata.create_date = datetime.date.today()
        content_metadata.file_groupid_fk_id = self.file_group
        content_metadata.file_location = self.get_url(file_path)
        content_metadata.file_name = os.path.basename(file_path)
        content_metadata.file_use = self.file_use
        content_metadata.file_sequence = self.file_sequence
        content_metadata.file_size = os.path.getsize(file_path)
        content_metadata.location_type = "URL"
        content_metadata.mime_type = mime_type

        return content_metadata
    
    def create_audio_mp3(self, dest_file_name):
        
        logger.info(f"Mp3 generation with source and output files: ('{self.src_file_name}', '{dest_file_name} )")

        try:
            self.create_dest_dir(dest_file_name)
            
            # Minimum acceptable parameters for wav conversion
            # acodec : libmp3lame - Standard mp3 encoder selection
            # audio_bitrate : 320k - High(er) constant bitrate chosen over VBR for device compatiblity reasons
            # ar : 44.1kHz - Matches sample rate of our source file, which will always be 16 bit 44.1khz wav for this project
            # ac : 2 channels - Forces to 2 channels in the case there are more or less present. OH source files will always be 2 channels
            # overwrite_output : True - Overwrite if existing file

            stream = ffmpeg.input(self.src_file_name)
            stream = ffmpeg.output(stream, dest_file_name, acodec='libmp3lame', audio_bitrate='320k', ar=44100, ac=2)
            ffmpeg.run(stream, overwrite_output=True)

            audio_metadata = self.populate_content_file_data(dest_file_name)

            logger.info(f'Audio processed: {dest_file_name}')

            return audio_metadata

        except:
            raise CommandError(f'Error processing file')
    
    def create_dest_dir(self, dest_file_name):
        
        p = Path(dest_file_name)
        parent_path = p.parent
        parent_path.mkdir(parents=True, exist_ok=True)


    def get_url(self, file_path):
        # May be fragile: assumes file_path starts with two elements we don't want
        # Example: /media/oh_lz/oralhistory-test/masters/21198-zz002kp5wz-1-master.tif
        # becomes oralhistory-test/masters/21198-zz002kp5wz-1-master.tif
        # TODO: Refactor to make this generic via an included library.
        
        # Currently supported only for Submaster
        if self.file_use in ['Submaster']:
            # Strip off first two elements of / delimited path, join the rest with /
            url_path = '/'.join(file_path.split('/')[3:])
            # Audio uses wowza, not static
            domain = 'https://wowza.library.ucla.edu'
            path_prefix = 'dlp/definst/mp3:oralhistory'
            path_suffix = 'playlist.m3u8'
            return f'{domain}/{path_prefix}/{url_path}/{path_suffix}'
        else:
            return file_path
