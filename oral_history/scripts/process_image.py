#!/usr/bin/env python3

from django.core.management.base import CommandError
from wand.image import Image


class ProcessImage():

    def __init__(self):
        print("Processing image file ...")

    def run(self, src_file_name, dest_file_name, resize_height, resize_width):
        print(f"script('{src_file_name}', '{dest_file_name}', '{resize_height}', {resize_width} )")

        try:
            with Image(filename = src_file_name) as img:
                img.resize(height = resize_height, width = resize_width)
                img.save(filename = dest_file_name)

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
