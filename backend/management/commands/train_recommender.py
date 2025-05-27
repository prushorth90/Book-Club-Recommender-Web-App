"""Command to train the model of the recommender system."""
from unibook import views
from django.core.management.base import BaseCommand

class Command(BaseCommand):
    """Command to train the model of the recommender system."""

    def handle(self, *args, **options):
        views.recommender.retrain_model()
