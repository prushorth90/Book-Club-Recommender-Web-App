from django.core.management.base import BaseCommand, CommandError
from unibook.models import Book

class Command(BaseCommand):
    def handle(self, *args, **options):
        Book.objects.all().delete()
