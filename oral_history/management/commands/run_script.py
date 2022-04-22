from django.core.management.base import BaseCommand
from oral_history.scripts.process import Process


class Command(BaseCommand):
    help = "Run the Oral History script"

    def add_arguments(self, parser):
        parser.add_argument("-g", "--file_group", action="store_true",
                            help="File group")
        parser.add_argument("-f", "--file_name", action="store_true",
                            help="File name")
        parser.add_argument("-a", "--item_ark", action="store_true",
                            help="Item ARK")

    def handle(self, *args, **options):
        file_group = options["file_group"],
        file_name = options["file_name"],
        item_ark = options["item_ark"],

        file_group_str = ''.join(map(str, file_group))
        file_name_str = ''.join(map(str, file_name))
        item_ark_str = ''.join(map(str, item_ark))

        #
        try:
            process = Process("reports")
            process.run(file_group_str, file_name_str, item_ark_str)
            return
        except ValueError as e:
            exit(e)
