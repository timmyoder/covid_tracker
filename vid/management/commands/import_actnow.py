from django.core.management.base import BaseCommand, CommandError

from vid.get_data import load_all_actnow


class Command(BaseCommand):

    def handle(self, *args, **options):
        load_all_actnow()
