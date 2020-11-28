"""
Import json data from JSON file to Datababse

from here: https://github.com/NEbere/data-import
"""

from django.core.management.base import BaseCommand

import vid.get_data
from vid.models import PennCases


class Command(BaseCommand):

    # def add_arguments(self, parser):
    #     parser.add_argument('api', nargs='+', type=str)

    def handle(self, *args, **options):
        """
        Call the function to import data
        """
        # for api in options['api']:
        PennCases.objects.all().delete()

        vid.get_data.refresh_penn_cases()


