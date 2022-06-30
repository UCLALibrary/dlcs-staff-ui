#!/usr/bin/env python3

import datetime
import logging
import mimetypes
import os
import shutil
from django.core.management.base import CommandError
from oral_history.models import ContentFiles
from pathlib import Path

logger = logging.getLogger(__name__)

class FileProcessor():

    def __init__(self, src_file_name, file_sequence, file_group, file_use, content_type):
        self.src_file_name = src_file_name
        self.file_sequence = file_sequence
        self.file_use = file_use
        self.file_group = file_group
        self.content_type = content_type

        logger.info(f'Copying file: {src_file_name}')

    def populate_content_file_data(self, file_path):
        
        mime_type, encoding = mimetypes.guess_type(file_path)

        content_metadata = ContentFiles()

        content_metadata.content_type = self.content_type
        content_metadata.create_date = datetime.date.today()
        content_metadata.file_groupid_fk_id = self.file_group
        content_metadata.file_location = self.get_url(file_path)
        content_metadata.file_name = os.path.basename(file_path)
        content_metadata.file_sequence = self.file_sequence
        content_metadata.file_size = os.path.getsize(file_path)
        content_metadata.file_use = self.file_use
        content_metadata.location_type = "URL"
        content_metadata.mime_type = mime_type
        
        return content_metadata

    
    def copy_file(self, dest_file_name):
        
        logger.info(f"Copied file from source, destination: ('{self.src_file_name}', '{dest_file_name} )")

        try:
            self.create_dest_dir(dest_file_name)
            shutil.copyfile(self.src_file_name, dest_file_name)
            
            file_metadata = self.populate_content_file_data(dest_file_name)

            logger.info(f'File copied: {dest_file_name}')

            return file_metadata

        except:
            raise CommandError(f'Error copying file')
    
    def create_dest_dir(self, dest_file_name):
        
        p = Path(dest_file_name)
        parent_path = p.parent
        parent_path.mkdir(parents=True, exist_ok=True)


    def get_url(self, file_path):
        # May be fragile: assumes file_path starts with two elements we don't want
        # Example: media/oh_lz/oralhistory-test/masters/21198-zz002kp5wz-1-master.tif
        # becomes oralhistory-test/masters/21198-zz002kp5wz-1-master.tif
        # TODO: Refactor to make this generic via an included library.
        
        # Currently supported only for Submaster and Thumbnail
        if self.file_use in ['Submaster', 'Thumbnail']:
            # Strip off first two elements of / delimited path, join the rest with /
            url_path = '/'.join(file_path.split('/')[2:])
            domain = 'https://static.library.ucla.edu'
            url = f'{domain}/{url_path}'
            logger.info(f'{file_path = }, {url = }')
            return url
        else:
            return file_path
