import requests

from django.core.management.base import BaseCommand


class Command(BaseCommand):
    """ class Command """

    def handle(self, *args, **options):
        requests.get('https://qanda-tb.herokuapp.com/')
        requests.get('https://qanda-tb.herokuapp.com/new/')
