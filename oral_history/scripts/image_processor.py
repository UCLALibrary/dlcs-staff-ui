#!/usr/bin/env python3

import logging
import mimetypes
import os
from django.core.management.base import CommandError
from oral_history.models import ContentFiles
from wand.image import Image

logger = logging.getLogger(__name__)

class ImageProcessor():

    THUMBNAIL_CATEGORY = "Thumbnail"
    SUBMASTER_CATEGORY = "Submaster"
    MASTER_CATEGORY = "Master"


    def __init__(self, src_file_name):
        self.src_file_name = src_file_name
        logger.info("Processing image file ...")


    def create_thumbnail(self, dest_file_name, resize_height, resize_width):
        
        return self.resize_image(dest_file_name, resize_height, resize_width, ImageProcessor.THUMBNAIL_CATEGORY)
    

    def populate_content_file_data(file_path, image_category):
        
        mime_type, encoding = mimetypes.guess_type(file_path)

        ContentFiles img_metadata = ContentFiles()
        img_metadata.mime_types = mime_type
        img_metadata.file_sequence = 0
        img_metadata.file_size = os.path.getsize(file_path)
        img_metadata.create_date = os.path.ctime(file_path)
        img_metadata.file_location = file_path
        img_metadata.location_type = image_category
        img_metadata.content_type = "Image"

        return img_metadata
    
    def resize_image(self, dest_file_name, resize_height, resize_width, process_category):
        
        logger.info(f"script('{self.src_file_name}', '{dest_file_name}', '{resize_height}', {resize_width} )")

        try:
            with Image(filename=self.src_file_name) as img:
                img.resize(height=resize_height, width=resize_width)
                img.save(filename=dest_file_name)

                ContentFiles img_metadata = self.populate_content_file_data(dest_file_name, process_category)
                
                return(img_metadata)

        except:
            raise CommandError(f'Error processing file')
        
        logger.info(f'Image processed: {dest_file_name}')
        # error detection goes here
        #
        # temporary example errors, uncomment to view in console; replace with the script being written by KristianA
        #
        #x = 1/0
        #
        # raise CommandError(
        #    f'Error from script - File not found: "{file_name}"')
        # raise CommandError(
        #    f'Error from script - This ARK format not supported: "{item_ark}"')

    