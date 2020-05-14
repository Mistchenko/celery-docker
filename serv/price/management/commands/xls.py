from django.core.management.base import BaseCommand
from django.conf import settings
from price.price_file_prepare import parser_xlsx

class Command(BaseCommand):
    help = 'Распарсить Excel'

    def handle(self, *args, **kwargs):
        print(self.help)
        #print(parser_xlsx({'id': 2}))
        print(parser_xlsx({'id': 3}))
