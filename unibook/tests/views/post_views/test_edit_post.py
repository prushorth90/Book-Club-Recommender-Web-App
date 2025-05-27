"""Unit tests for edit post view."""
from django.urls import reverse
from unibook.models import Post, User, Club, User_Auth
from unibook.tests.helpers import LogInTester
from rest_framework import status
from rest_framework.test import APITestCase

class EditPostTests(APITestCase, LogInTester):
    """Unit tests for edit post view."""

    fixtures = ['unibook/tests/fixtures/default_user.json',
                'unibook/tests/fixtures/other_users.json',
                'unibook/tests/fixtures/default_club.json',
                'unibook/tests/fixtures/other_clubs.json']

    def setUp(self):
        self.user = User.objects.get(username='baldunicorn')
        self.club = Club.objects.get(name='Book Club 1')
        self.other_user = User.objects.get(username = 'fluffyunicorn')
        self.other_club = Club.objects.get(name = 'Book Club 2')
        User_Auth.objects.create(user=self.user, rank='owner', club=self.club)
        self.data = {'author': self.user,
                    'text': 'Hi there! I am I unicorn who is very bald',
                    'club': self.club}
        self.post = Post.objects.create(author=self.data['author'], text='The original text', club=self.data['club'])
        self.url = reverse('edit_post', kwargs={'post_id': self.post.id})

    def test_edit_post_url(self):
        """Test for the edit post url."""

        self.assertEqual(self.url, '/unibook/edit-post/1')

    def test_successful_edit_post(self):
        """Test for user successfully editing the post they created."""

        self.client.login(username=self.user.username, password='Password123')
        self.assertTrue(self._is_logged_in())
        post_text_before = Post.objects.latest('created_at').text
        post_count_before = Post.objects.count()
        response = self.client.put(self.url, self.data)
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        post_text_after = Post.objects.latest('created_at').text
        post_count_after = Post.objects.count()
        self.assertNotEqual(post_text_before, post_text_after)
        self.assertEqual(post_count_before, post_count_after)

    def test_cannot_edit_another_users_post(self):
        """Test for user not being able to edit another user's post."""

        self.client.login(username=self.other_user.username, password='Password123')
        self.assertTrue(self._is_logged_in())
        post_text_before = Post.objects.latest('created_at').text
        post_count_before = Post.objects.count()
        response = self.client.put(self.url, self.data)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        post_text_after = Post.objects.latest('created_at').text
        post_count_after = Post.objects.count()
        self.assertEqual(post_text_before, post_text_after)
        self.assertEqual(post_count_before, post_count_after)
