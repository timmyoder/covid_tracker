from django.core.management.base import BaseCommand, CommandError

from vid.get_data import (load_all_actnow,
                          load_nyt,
                          refresh_penn_cases,
                          refresh_penn_hospital,
                          refresh_penn_deaths,
                          cache_pages)


class Command(BaseCommand):

    def add_arguments(self, parser):
        # Named (optional) arguments
        parser.add_argument(
            '--local',
            action='store_true',
            help='Run refresh locally',
        )

    def handle(self, *args, **options):
        # load pa data
        refresh_penn_cases()
        refresh_penn_deaths()
        refresh_penn_hospital()

        # load Covid ActNow metrics
        load_all_actnow()

        # load NYT deaths and cases
        load_nyt()

        # render and cache pages
        cache_pages(running_local=options['local'])
