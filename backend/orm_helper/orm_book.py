from unibook.models import Book
from django.core.exceptions import ObjectDoesNotExist, MultipleObjectsReturned
from .orm_user import *
import csv
import pandas as pd

def get_book(book_id):
    """Get the book object from book id."""

    try:
        book = Book.objects.get(id=book_id)
        return book
    except ObjectDoesNotExist:
        return None

def get_book_from_title(book_title):
    """Get the book object from book title."""

    try:
        book = Book.objects.get(title=book_title)
        return book
    except ObjectDoesNotExist:
        return None
    except MultipleObjectsReturned:
        book = Book.objects.filter(title=book_title).first()
        return book

def get_books_from_isbn(books_isbn):
    """Get the book objects from a list of isbn."""

    books = []
    for book_isbn in books_isbn:
        try:
            book = Book.objects.get(isbn=book_isbn)
            books.append(book)
        except:
            pass

    return books

def add_to_book_rating_csv(book, rating, user_id):
    """Add the book rated from the user to the csv file."""

    path = 'unibook/recommender/book_dataset/BX_Book_Ratings.csv'
    with open(path, 'a') as csvfile:
        writer = csv.writer(csvfile, delimiter=";")
        # Will delete once add search engine
        # if book == None:
        #     return None
        if book.title in get_books_to_show(user_id):
            return None
        writer.writerow([user_id, book.isbn, rating])
        return book

def get_books_to_show(user_id):
    """Get the books to show to the user that they have rated."""

    ratings_path = 'unibook/recommender/book_dataset/BX_Book_Ratings.csv'

    ratings = pd.read_csv(ratings_path, sep=';', encoding='ISO-8859-1')
    books_rated = ratings[ratings['User-ID'] == user_id]
    books_to_show = []
    for book_isbn in books_rated['ISBN']:
        book = Book.objects.get(isbn=book_isbn)
        books_to_show.append(book.title)
    return books_to_show
