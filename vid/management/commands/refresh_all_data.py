from django.core.management.base import BaseCommand, CommandError

from vid.get_data import (load_all_actnow,
                          load_nyt,
                          refresh_penn_cases,
                          refresh_penn_hospital,
                          refresh_penn_deaths)


class Command(BaseCommand):

    # def add_arguments(self, parser):
    #     parser.add_argument('csv_file', nargs='+', type=str)

    def handle(self, *args, **options):
        # load pa data
        refresh_penn_cases()
        refresh_penn_deaths()
        refresh_penn_hospital()

        # load Covid ActNow metrics
        load_all_actnow()

        # load NYT deaths and cases
        load_nyt()
