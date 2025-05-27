"""Database Seeder"""
import csv
from unibook.models import Book
from django.core.management.base import BaseCommand


class Command(BaseCommand):
    """Database Seeder"""
    def handle(self, *args, **options):
        books = []
        with open('unibook/recommender/book_dataset/BX_Books.csv', encoding='ISO-8859-1') as f:
            reader = csv.reader(f, delimiter=';')
            next(reader)
            for row in reader:
                books.append(Book(isbn=row[0], title=row[1], image_url=row[5]))

                if len(books) > 10000:
                    Book.objects.bulk_create(books)
                    books = []
            Book.objects.bulk_create(books)
