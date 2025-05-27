from django.core.management.base import BaseCommand, CommandError
from unibook.models import User, Club, User_Auth

class Command(BaseCommand):
    def handle(self, *args, **options):
        User.objects.filter(is_staff=False, is_superuser=False).delete()
        Club.objects.all().delete()
        User_Auth.objects.all().delete()
