#!/usr/bin/env python3

from django.core.management.base import CommandError
from oral_history.models import ContentFiles
from wand.image import Image


class ImageProcessor():

    def __init__(self, src_file_name):
        self.src_file_name = src_file_name
        print("Processing image file ...")

    def populate_content_file_data(wand_img_obj) {
        ContentFiles img_metadata = ContentFiles()
        img_metadata.mime_types = "Placeholder"
        img_metadata.file_sequence = 0
        img_metadata.file_size = 0
        img_metadata.create_date = ""
        img_metadata.file_location = "Placeholder"
        img_metadata.location_type = "Placeholder"
        img_metadata.content_type = "Image"

        return img_metadata

    }

    def resize_image(self, dest_file_name, resize_height, resize_width):
        
        print(f"script('{src_file_name}', '{dest_file_name}', '{resize_height}', {resize_width} )")

        try:
            with Image(filename = self.src_file_name) as img:
                img.resize(height = resize_height, width = resize_width)
                img.save(filename = dest_file_name)

                ContentFiles img_metadata = populate_content_file_data(img)
                return(img_metadata)

        except:
            raise CommandError(f'Error processing file')
        
        print(f'Image processed: {dest_file_name}')
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

    