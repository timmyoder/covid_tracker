from django.core.management.base import BaseCommand

from vid.get_data import load_metrics, load_nyt_all_us, cache_pages


class Command(BaseCommand):

    def add_arguments(self, parser):
        # Named (optional) arguments
        parser.add_argument(
            '--local',
            action='store_true',
            help='Run refresh locally',
        )

    def handle(self, *args, **options):
        # load NYT deaths and cases
        load_metrics()
        load_nyt_all_us()

        # render and cache pages
        cache_pages(running_local=options['local'])
