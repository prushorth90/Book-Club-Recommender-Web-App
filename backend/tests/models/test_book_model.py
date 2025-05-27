"""Unit tests for Book model."""
from unibook.models import Book
from django.core.exceptions import ValidationError
from rest_framework.test import APITestCase

class BookModelTestCase(APITestCase):
    """Unit tests for Book model."""

    fixtures = [
        'unibook/tests/fixtures/default_book.json',
        'unibook/tests/fixtures/other_books.json',
    ]

    def setUp(self):
        self.book = Book.objects.get(isbn='0195153448')
        self.second_book = Book.objects.get(isbn='0002005018')

    def assert_book_is_valid(self):
        """Raise an error if book is invalid."""

        try:
            self.book.full_clean()
        except (ValidationError):
            self.fail('Test book needs to be made valid')

    def assert_book_is_invalid(self):
        """Raise an error if book is valid."""

        with self.assertRaises(ValidationError):
            self.book.full_clean()

    def test_valid_book(self):
        """Test if the current book is valid."""

        self.assert_book_is_valid()

    """ Unit test for isbn """

    def test_isbn_must_be_unique(self):
        self.book.isbn = self.second_book.isbn
        self.assert_book_is_invalid()

    def test_isbn_must_not_be_greater_than_13_characters(self):
        self.book.isbn = 'u' * 14
        self.assert_book_is_invalid()

    def test_isbn_can_have_13_characters(self):
        self.book.isbn = 'u' * 13
        self.assert_book_is_valid()

    def test_isbn_must_not_be_blank(self):
        self.book.isbn = ''
        self.assert_book_is_invalid()

    """ Unit test for title """

    def test_title_need_not_be_unique(self):
        self.book.title = self.second_book.title
        self.assert_book_is_valid()

    def test_title_must_not_be_blank(self):
        self.book.title = ''
        self.assert_book_is_invalid()

    """ Unit test for image_url """

    def test_image_url_need_not_be_unique(self):
        self.book.image_url = self.second_book.image_url
        self.assert_book_is_valid()

    def test_image_url_must_have_scheme(self):
        self.book.image_url = 'images.amazon.com/images/P/0195153448.01.MZZZZZZZ.jpg'
        self.assert_book_is_invalid()

    def test_image_url_must_have_domain_name(self):
        self.book.image_url = 'http://images/P/0195153448.01.MZZZZZZZ.jpg'
        self.assert_book_is_invalid()

    def test_image_url_must_not_have_two_consecutive_dots(self):
        self.book.image_url = 'http://images..amazon.com/images/P/0195153448.01.MZZZZZZZ.jpg'
        self.assert_book_is_invalid()

    def test_image_url_must_not_have_dot_before_domain_name(self):
        self.book.image_url = 'http://.images.amazon.com/images/P/0195153448.01.MZZZZZZZ.jpg'
        self.assert_book_is_invalid()

    def test_image_url_can_be_blank(self):
        self.book.image_url = ''
        self.assert_book_is_valid()
