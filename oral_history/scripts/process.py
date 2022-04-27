#!/usr/bin/env python3

from django.core.management.base import CommandError


class Process():

    def __init__(self, reports_dir):
        print("Processing media file ...")

    def run(self, file_group, file_name, item_ark):
        print(f"script('{file_group}', '{file_name}', '{item_ark}')")

        # error detection goes here
        # temporary example error, uncomment to view in console

        # raise CommandError('file "%s" not found' % file_name)
