import string
from django.core.management.base import BaseCommand, CommandError

class Command(BaseCommand):
    help = 'Scaffolding for file processing command...'

    def add_arguments(self, parser):
        parser.add_argument('file_name', type=string)
    
    def handle(self, *args, **options):
        file_name = options['file_name']
        self.stdout.write("File submitted is %s" % file_name)

