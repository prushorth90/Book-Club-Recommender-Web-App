"""Unit tests for delete post view."""
from django.urls import reverse
from unibook.models import Post, User, Club, User_Auth
from unibook.tests.helpers import LogInTester
from rest_framework import status
from rest_framework.test import APITestCase

class DeletePostTests(APITestCase, LogInTester):
    """Unit tests for delete post view."""

    fixtures = ['unibook/tests/fixtures/default_user.json',
                'unibook/tests/fixtures/other_users.json',
                'unibook/tests/fixtures/default_club.json',
                'unibook/tests/fixtures/other_clubs.json']

    def setUp(self):
        self.user = User.objects.get(username='baldunicorn')
        self.club = Club.objects.get(name='Book Club 1')
        self.other_user = User.objects.get(username = 'fluffyunicorn')
        User_Auth.objects.create(user=self.user, rank='owner', club=self.club)
        self.post = Post.objects.create(author=self.user, text='The original text', club=self.club)
        self.url = reverse('delete_post', kwargs={'post_id': self.post.id})

    def test_delete_post_url(self):
        """Test for the delete post url."""

        self.assertEqual(self.url, '/unibook/delete-post/1')

    def test_user_can_delete_own_post(self):
        """Test for user successfully deleting their own post."""

        self.client.login(username=self.user.username, password='Password123')
        self.assertTrue(self._is_logged_in())
        post_count_before = Post.objects.count()
        response = self.client.delete(self.url)
        post_count_after = Post.objects.count()
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(post_count_after, post_count_before-1)

    def test_user_cannot_delete_another_users_post(self):
        """Test user not being able to delete another user's post"""

        self.client.login(username=self.other_user.username, password='Password123')
        self.assertTrue(self._is_logged_in())
        post_count_before = Post.objects.count()
        response = self.client.delete(self.url)
        post_count_after = Post.objects.count()
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(post_count_before, post_count_after)
