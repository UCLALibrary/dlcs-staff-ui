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
        content_metadata.file_groupid_fk_id = self.file_group
        content_metadata.file_use = self.file_use
        content_metadata.file_sequence = self.file_sequence
        content_metadata.content_type = self.content_type

        content_metadata.mime_type = mime_type
        content_metadata.file_size = os.path.getsize(file_path)
        content_metadata.create_date = datetime.date.today()
        content_metadata.file_location = file_path

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

        
        
