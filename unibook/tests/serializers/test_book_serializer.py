"""Unit tests for book serializer."""
from unibook.models import Book
from unibook.serializers import BookSerializer
from rest_framework.test import APITestCase

class BookSerializerTestCase(APITestCase):
    """Unit tests for book serializer."""

    def setUp(self):
        self.serializer_data = {
            'isbn': '0061964360',
            'title': 'Pride and Prejudice (Teen Classics)',
            'image_url': 'https://pictures.abebooks.com/isbn/9780061964367-uk.jpg'
        }

    def test_valid_book_serializer(self):
        """Test the serializer to create a valid book."""

        serializer = BookSerializer(data=self.serializer_data)
        self.assertTrue(serializer.is_valid())

    def test_serializer_has_necessary_fields(self):
        """Test the serializer to check if it has necessary fields."""

        serializer = BookSerializer()
        self.assertIn('isbn', serializer.fields)
        self.assertIn('title', serializer.fields)
        self.assertIn('image_url', serializer.fields)

    def test_serializer_saves_correctly(self):
        """Test that the serializer saves correctly."""

        serializer = BookSerializer(data=self.serializer_data)
        before_count = Book.objects.count()
        serializer.is_valid()
        serializer.save()
        after_count = Book.objects.count()
        self.assertEqual(after_count, before_count + 1)
        book = Book.objects.get(isbn='0061964360')
        self.assertEqual(book.isbn, '0061964360')
        self.assertEqual(book.title, 'Pride and Prejudice (Teen Classics)')
        self.assertEqual(book.image_url, 'https://pictures.abebooks.com/isbn/9780061964367-uk.jpg')

    def test_isbn_must_contain_at_most_13_characters(self):
        """Test for the invalid serializer that can't be saved when the isbn contains more than 13 characters."""

        self.serializer_data['isbn'] = '0' * 14
        serializer = BookSerializer(data=self.serializer_data)
        self.assertFalse(serializer.is_valid())
        before_count = Book.objects.count()
        with self.assertRaises(AssertionError):
            serializer.save()
        after_count = Book.objects.count()
        self.assertEqual(after_count, before_count)

    def test_isbn_must_not_be_blank(self):
        """Test for the invalid serializer that can't be saved when the isbn is blank."""

        self.serializer_data['isbn'] = ''
        serializer = BookSerializer(data=self.serializer_data)
        self.assertFalse(serializer.is_valid())
        before_count = Book.objects.count()
        with self.assertRaises(AssertionError):
            serializer.save()
        after_count = Book.objects.count()
        self.assertEqual(after_count, before_count)

    def test_title_must_not_be_blank(self):
        """Test for the invalid serializer that can't be saved when the title is blank."""

        self.serializer_data['title'] = ''
        serializer = BookSerializer(data=self.serializer_data)
        self.assertFalse(serializer.is_valid())
        before_count = Book.objects.count()
        with self.assertRaises(AssertionError):
            serializer.save()
        after_count = Book.objects.count()
        self.assertEqual(after_count, before_count)

    """ Unit tests for image url """

    def test_image_url_can_be_blank(self):
        self.serializer_data['image_url'] = ''
        serializer = BookSerializer(data=self.serializer_data)
        self.assertTrue(serializer.is_valid())
        before_count = Book.objects.count()
        serializer.save()
        after_count = Book.objects.count()
        self.assertEqual(after_count, before_count+1)

    def test_image_url_must_have_scheme(self):
        self.serializer_data['image_url'] = 'images.amazon.com/images/P/0195153448.01.MZZZZZZZ.jpg'
        serializer = BookSerializer(data=self.serializer_data)
        self.assertFalse(serializer.is_valid())
        before_count = Book.objects.count()
        with self.assertRaises(AssertionError):
            serializer.save()
        after_count = Book.objects.count()
        self.assertEqual(after_count, before_count)

    def test_image_url_must_have_domain_name(self):
        self.serializer_data['image_url'] = 'http://images/P/0195153448.01.MZZZZZZZ.jpg'
        serializer = BookSerializer(data=self.serializer_data)
        self.assertFalse(serializer.is_valid())
        before_count = Book.objects.count()
        with self.assertRaises(AssertionError):
            serializer.save()
        after_count = Book.objects.count()
        self.assertEqual(after_count, before_count)

    def test_image_url_must_not_have_two_consecutive_dots(self):
        self.serializer_data['image_url'] = 'http://images..amazon.com/images/P/0195153448.01.MZZZZZZZ.jpg'
        serializer = BookSerializer(data=self.serializer_data)
        self.assertFalse(serializer.is_valid())
        before_count = Book.objects.count()
        with self.assertRaises(AssertionError):
            serializer.save()
        after_count = Book.objects.count()
        self.assertEqual(after_count, before_count)

    def test_image_url_must_not_have_dot_before_domain_name(self):
        self.serializer_data['image_url'] = 'http://.images.amazon.com/images/P/0195153448.01.MZZZZZZZ.jpg'
        serializer = BookSerializer(data=self.serializer_data)
        self.assertFalse(serializer.is_valid())
        before_count = Book.objects.count()
        with self.assertRaises(AssertionError):
            serializer.save()
        after_count = Book.objects.count()
        self.assertEqual(after_count, before_count)
