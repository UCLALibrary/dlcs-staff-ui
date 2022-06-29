#!/usr/bin/env python3

import datetime
import logging
import mimetypes
import os
from django.core.management.base import CommandError
from oral_history.models import ContentFiles
from pathlib import Path
from wand.image import Image

logger = logging.getLogger(__name__)

class ImageProcessor():

    THUMBNAIL_CATEGORY = "Thumbnail"
    SUBMASTER_CATEGORY = "Submaster"
    MASTER_CATEGORY = "Master"

    IMAGE_CONTENT_TYPE = "Image"


    def __init__(self, src_file_name, file_sequence, file_group):
        self.src_file_name = src_file_name
        self.file_sequence = file_sequence
        self.file_group = file_group

        logger.info(f'Processing image: {src_file_name}')

    def create_thumbnail(self, dest_file_name, resize_height, resize_width):
        
        return self.resize_image(dest_file_name, resize_height, resize_width, ImageProcessor.THUMBNAIL_CATEGORY)
    
    def create_submaster_img(self, dest_file_name, resize_height, resize_width):

        return self.resize_image(dest_file_name, resize_height, resize_width, ImageProcessor.SUBMASTER_CATEGORY)
    
    def populate_content_file_data(self, file_path, image_category):
        
        mime_type, encoding = mimetypes.guess_type(file_path)

        img_metadata = ContentFiles()
        img_metadata.mime_type = mime_type
        img_metadata.file_sequence = self.file_sequence
        img_metadata.file_groupid_fk_id = self.file_group
        img_metadata.file_size = os.path.getsize(file_path)
        img_metadata.create_date = datetime.date.today()
        img_metadata.file_location = file_path
        img_metadata.location_type = image_category
        img_metadata.content_type = self.IMAGE_CONTENT_TYPE

        return img_metadata
    
    def resize_image(self, dest_file_name, resize_height, resize_width, process_category):
        
        logger.info(f"script('{self.src_file_name}', '{dest_file_name}', '{resize_height}', {resize_width}, {process_category} )")

        try:
            self.create_dest_dir(dest_file_name)

            resize_height = int(resize_height)
            resize_width = int(resize_width)
            
            with Image(filename=self.src_file_name) as img:
                img.resize(height=resize_height, width=resize_width)
                img.save(filename=dest_file_name)
                
                img_metadata = self.populate_content_file_data(dest_file_name, process_category)
                return img_metadata

        except:
            raise CommandError(f'Error processing file')
        
    def create_dest_dir(self, dest_file_name):
        
        p = Path(dest_file_name)
        parent_path = p.parent
        parent_path.mkdir(parents=True, exist_ok=True)
