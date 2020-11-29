from django.core.management.base import BaseCommand, CommandError

from vid.get_data import load_actnow, focus_fips
from vid.models import MetricsActNow


class Command(BaseCommand):

    # def add_arguments(self, parser):
    #     parser.add_argument('csv_file', nargs='+', type=str)

    def handle(self, *args, **options):
        MetricsActNow.objects.all().delete()

        for fips in focus_fips:
            load_actnow(fips=fips)
