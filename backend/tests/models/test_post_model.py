"""Unit tests of the Post model"""
from django.core.exceptions import ValidationError, ObjectDoesNotExist
from unibook.models import Post, User, Club
from rest_framework.test import APITestCase

class PostModelTestCase(APITestCase):
    """Unit tests of the Post model"""

    fixtures = [
        'unibook/tests/fixtures/default_user.json',
        'unibook/tests/fixtures/default_club.json'
    ]

    def setUp(self):
        self.user = User.objects.get(username='baldunicorn')
        self.club = Club.objects.get(name='Book Club 1')
        self.post = Post.objects.create(
            author = self.user,
            club = self.club,
            text = 'This is a post by the baldest of unicorns'
        )
        self.second_post = Post.objects.create(
            author = self.user,
            club = self.club,
            text = 'I AM FALLING ASLEEP.'
        )

    def assert_post_is_valid(self):
        """Raise an error if the post is invalid."""

        try:
            self.post.full_clean()
        except (ValidationError):
            self.fail('Test post should be valid')

    def assert_post_is_invalid(self):
        """Raise an error if the post is valid."""

        with self.assertRaises(ValidationError):
            self.post.full_clean()

    def test_valid_post(self):
        """Test is the post set up is valid."""

        self.assert_post_is_valid()

    """ Unit test for author """

    def test_author_must_not_be_blank(self):
        self.post.author = None
        self.assert_post_is_invalid()

    def test_post_is_deleted_if_author_is_deleted(self):
        self.user.delete()
        with self.assertRaises(ObjectDoesNotExist):
            Post.objects.get(id=self.post.id)

    """ Unit test for text """

    def test_text_need_not_be_unique(self):
        self.post.text = self.second_post.text
        self.assert_post_is_valid()

    def test_text_must_not_be_blank(self):
        self.post.text = ''
        self.assert_post_is_invalid()

    def test_text_must_not_be_greater_than_280_characters(self):
        self.post.text = 'x' * 281
        self.assert_post_is_invalid()

    def test_text_can_be_280_characters(self):
        self.post.text = 'x' * 280
        self.assert_post_is_valid()

    """ Unit test for created_at """

    def test_created_at_need_not_be_unique(self):
        self.post.created_at = self.second_post.created_at
        self.assert_post_is_valid()

    """ Unit test for club """

    def test_club_must_not_be_blank(self):
        self.post.club = None
        self.assert_post_is_invalid()

    def test_post_is_deleted_if_club_is_deleted(self):
        self.club.delete()
        with self.assertRaises(ObjectDoesNotExist):
            Post.objects.get(id=self.post.id)
