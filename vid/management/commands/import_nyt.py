from django.core.management.base import BaseCommand, CommandError

from vid.get_data import load_metrics


class Command(BaseCommand):

    # def add_arguments(self, parser):
    #     parser.add_argument('csv_file', nargs='+', type=str)

    def handle(self, *args, **options):
        load_metrics()
