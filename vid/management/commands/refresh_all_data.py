from django.core.management.base import BaseCommand

from vid.get_data import load_metrics, load_nyt_all_us, cache_pages, CURRENT_YEAR, PREVIOUS_YEARS


class Command(BaseCommand):

    def add_arguments(self, parser):
        # Named (optional) arguments
        parser.add_argument(
            '--local',
            action='store_true',
            help='Run refresh locally',
        )

        # Named (optional) arguments
        parser.add_argument(
            '--previous_years',
            action='store_true',
            help='download data for a previous year instead of the current year',
        )

    def handle(self, *args, **options):
        # load NYT county deaths and cases
        if options['previous_years']:
            for year in PREVIOUS_YEARS:
                load_metrics(year)
        else:
            load_metrics()

        # the full us data
        load_nyt_all_us()

        # render and cache pages
        cache_pages(running_local=options['local'])
