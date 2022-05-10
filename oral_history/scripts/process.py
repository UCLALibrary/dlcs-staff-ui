#!/usr/bin/env python3

from django.core.management.base import CommandError


class Process():

    def __init__(self, reports_dir):
        print("Processing media file ...")

    def run(self, file_group, file_name, item_ark):
        print(f"script('{file_group}', '{file_name}', '{item_ark}')")

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
