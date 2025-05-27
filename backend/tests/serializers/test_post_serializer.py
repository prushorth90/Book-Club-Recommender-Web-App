"""Unit tests for post serializer."""
from unibook.models import Club, User, Post
from unibook.serializers import PostSerializer
from rest_framework.test import APITestCase

class PostSerializerTestCase(APITestCase):
    """Unit tests for book serializer."""

    fixtures = [
        'unibook/tests/fixtures/default_user.json',
        'unibook/tests/fixtures/default_club.json'
    ]

    def setUp(self):
        self.user = User.objects.get(username='baldunicorn')
        self.club = Club.objects.get(name='Book Club 1')

        self.serializer_data = {
            'author': self.user,
            'club': self.club,
            'text': 'Hello'
        }

    def test_valid_post_serializer(self):
        """Test the serializer to create a valid post"""

        serializer = PostSerializer(data=self.serializer_data)
        self.assertTrue(serializer.is_valid())

    def test_serializer_has_necessary_fields(self):
        """Test the serializer to check if it has necessary fields."""

        serializer = PostSerializer()
        self.assertIn('author', serializer.fields)
        self.assertIn('club', serializer.fields)
        self.assertIn('text', serializer.fields)

    def test_serializer_saves_correctly(self):
        """Test that the serializer saves correctly."""

        serializer = PostSerializer(data=self.serializer_data)
        before_count = Post.objects.count()
        serializer.is_valid()
        serializer.save()
        after_count = Post.objects.count()
        self.assertEqual(after_count, before_count + 1)
        post = Post.objects.get(id=1)
        self.assertEqual(post.author, self.user)
        self.assertEqual(post.club, self.club)
        self.assertEqual(post.text, 'Hello')

    def test_text_must_not_be_blank(self):
        """Test that the text not blank."""

        self.serializer_data['text'] = ''
        serializer = PostSerializer(data=self.serializer_data)
        before_count = Post.objects.count()
        with self.assertRaises(AssertionError):
            serializer.save()
        after_count = Post.objects.count()
        self.assertEqual(after_count, before_count)

    def test_text_must_not_be_greater_than_280_characters(self):
        """Test that the text not more than 280 characters"""

        self.serializer_data['text'] = 'a'*291
        serializer = PostSerializer(data=self.serializer_data)
        before_count = Post.objects.count()
        with self.assertRaises(AssertionError):
            serializer.save()
        after_count = Post.objects.count()
        self.assertEqual(after_count, before_count)

    def test_text_can_be_280_characters(self):
        """Test that the text can be 280 characters """

        self.serializer_data['text'] = 'a'*280
        serializer = PostSerializer(data=self.serializer_data)
        before_count = Post.objects.count()
        with self.assertRaises(AssertionError):
            serializer.save()
        after_count = Post.objects.count()
        self.assertEqual(after_count, before_count)
