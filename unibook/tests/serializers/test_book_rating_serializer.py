"""Unit tests for book rating serializer."""
from unibook.models import Book, User, BookRating
from unibook.serializers import BookRatingSerializer
from rest_framework.test import APITestCase

class BookSerializerTestCase(APITestCase):

    fixtures = [
        'unibook/tests/fixtures/default_user.json',
        'unibook/tests/fixtures/other_users.json',
        'unibook/tests/fixtures/default_club.json',
        'unibook/tests/fixtures/other_clubs.json',
        'unibook/tests/fixtures/default_book.json',
    ]

    def setUp(self):
        self.user = User.objects.get(username='baldunicorn')
        self.book = Book.objects.get(isbn= "0195153448")
        self.serializer_data = {
        'book': self.book.isbn,
        'rating': 7,
        }

    def test_valid_create_book_ratings_serializer(self):
        """Test the serializer to create a valid book rating."""

        serializer = BookRatingSerializer(data=self.serializer_data)
        self.assertTrue(serializer.is_valid())

    def test_serializer_has_necessary_fields(self):
        """Test the serializer to check if it has necessary fields."""

        serializer = BookRatingSerializer()
        self.assertIn('book', serializer.fields)
        self.assertIn('rating', serializer.fields)

    def test_serializer_saves_correctly(self):
        """Test that the serializer saves correctly."""

        serializer = BookRatingSerializer(data=self.serializer_data)
        before_count = BookRating.objects.count()
        serializer.is_valid()
        serializer.save()
        after_count = BookRating.objects.count()
        self.assertEqual(after_count, before_count + 1)
        bookRating = BookRating.objects.get(book=self.book.id)
        self.assertEqual(bookRating.book, self.book)
        self.assertEqual(bookRating.rating, 7)

    def test_rating_can_not_be_empty(self):
        """"Test for the invalid serializer that can't be saved when the rating is blank."""

        self.serializer_data['rating'] = ''
        serializer = BookRatingSerializer(data=self.serializer_data)
        self.assertFalse(serializer.is_valid())
        before_count = Book.objects.count()
        with self.assertRaises(AssertionError):
            serializer.save()
        after_count = Book.objects.count()
        self.assertEqual(after_count, before_count)

    def test_rating_has_max_value_of_10(self):
        """"Test for the invalid serializer that can't be saved when the rating is more than 10."""

        self.serializer_data['rating'] = 11
        serializer = BookRatingSerializer(data=self.serializer_data)
        self.assertFalse(serializer.is_valid())
        before_count = Book.objects.count()
        with self.assertRaises(AssertionError):
            serializer.save()
        after_count = Book.objects.count()
        self.assertEqual(after_count, before_count)

    def test_rating_has_min_value_of_1(self):
        """"Test for the invalid serializer that can't be saved when the rating is less than one."""

        self.serializer_data['rating'] = 0
        serializer = BookRatingSerializer(data=self.serializer_data)
        self.assertFalse(serializer.is_valid())
        before_count = Book.objects.count()
        with self.assertRaises(AssertionError):
            serializer.save()
        after_count = Book.objects.count()
        self.assertEqual(after_count, before_count)

    def test_rating_has_to_be_positive(self):
        """"Test for the invalid serializer that can't be saved when the rating is negative."""

        self.serializer_data['rating'] = -1
        serializer = BookRatingSerializer(data=self.serializer_data)
        self.assertFalse(serializer.is_valid())
        before_count = Book.objects.count()
        with self.assertRaises(AssertionError):
            serializer.save()
        after_count = Book.objects.count()
        self.assertEqual(after_count, before_count)
