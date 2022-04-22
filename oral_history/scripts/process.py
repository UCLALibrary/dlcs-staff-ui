#!/usr/bin/env python3


class Process():

    def __init__(self, reports_dir):
        print("Processing media file ...")

    def run(self, file_group, file_name, item_ark):
        print("script('"+str(file_group)+"', '" +
              str(file_name)+"', '"+str(item_ark)+"')")
