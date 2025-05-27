"""Unit tests for Book Rating model."""
from django.core.exceptions import ValidationError, ObjectDoesNotExist
from rest_framework.test import APITestCase
from unibook.models import BookRating, Book, User, Club

class BookRatingModelTestCase(APITestCase):
    """Unit tests for Book Rating model."""

    fixtures = [
        'unibook/tests/fixtures/default_user.json',
        'unibook/tests/fixtures/other_users.json',
        'unibook/tests/fixtures/default_book.json',
        'unibook/tests/fixtures/other_books.json',
    ]

    def setUp(self):
        self.creator = User.objects.get(username='baldunicorn')
        self.other_creator = User.objects.get(username='user3')
        self.book = Book.objects.get(isbn= "0195153448")
        self.other_book = Book.objects.get(isbn='0002005018')
        self.book_rating = BookRating.objects.create(
            creator = self.creator,
            book = self.book,
            rating = 7
        )
        self.other_book_rating = BookRating.objects.create(
            creator = self.other_creator,
            book = self.other_book,
            rating = 8
        )

    def assert_book_rating_is_valid(self):
        """Raise an error if book rating is invalid."""

        try:
            self.book_rating.full_clean()
        except (ValidationError):
            self.fail('Test book rating needs to be made valid')

    def assert_book_rating_is_invalid(self):
        """Raise an error if book rating is valid."""

        with self.assertRaises(ValidationError):
            self.book_rating.full_clean()

    def test_valid_book_rating(self):
        """Test if the current book is valid."""

        self.assert_book_rating_is_valid()

    """Unit Tests for creator"""

    def test_creator_can_not_be_blank(self):
        self.book_rating.creator = None
        self.assert_book_rating_is_invalid()

    def test_book_rating_is_deleted_if_creator_is_deleted(self):
        self.creator.delete()
        with self.assertRaises(ObjectDoesNotExist):
            BookRating.objects.get(id=self.book_rating.id)

    """Unit Tests for book"""

    def test_book_rating_is_deleted_if_book_is_deleted(self):
        self.book.delete()
        self.book_rating = BookRating.objects.get(id=self.book_rating.id)
        self.assertEqual(self.book_rating.book, None)

    def test_book_need_be_unique(self):
        self.book_rating.book = self.other_book_rating.book
        self.assert_book_rating_is_valid()

    """Unit tests for rating"""

    def test_rating_need_not_be_unique(self):
        self.book_rating.rating = self.other_book_rating.rating
        self.assert_book_rating_is_valid()

    def test_rating_cannot_be_greater_than_10(self):
        self.book_rating.rating = 11
        self.assert_book_rating_is_invalid()

    def test_rating_cannot_be_lesser_than_1(self):
        self.book_rating.rating = 0
        self.assert_book_rating_is_invalid()

    def test_rating_cannot_be_negative(self):
        self.book_rating.rating = -1
        self.assert_book_rating_is_invalid()

    def test_rating_can_be_10(self):
        self.book_rating.rating = 10
        self.assert_book_rating_is_valid()

    def test_rating_can_be_1(self):
        self.book_rating.rating = 1
        self.assert_book_rating_is_valid()

    def test_rating_cannot_be_letters(self):
        self.book_rating.rating = 'a'
        self.assert_book_rating_is_invalid()
