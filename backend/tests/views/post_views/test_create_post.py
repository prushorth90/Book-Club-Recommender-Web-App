"""Unit tests for create post view."""
from django.urls import reverse
from unibook.models import Post, User, Club, User_Auth
from unibook.tests.helpers import LogInTester
from rest_framework import status
from rest_framework.test import APITestCase

class CreatePostViewTests(APITestCase, LogInTester):
    """Unit tests for create post view."""

    fixtures = ['unibook/tests/fixtures/default_user.json',
                'unibook/tests/fixtures/other_users.json',
                'unibook/tests/fixtures/default_club.json',
                'unibook/tests/fixtures/other_clubs.json']

    def setUp(self):
        self.user = User.objects.get(username='baldunicorn')
        self.club = Club.objects.get(name='Book Club 1')
        self.other_user = User.objects.get(username = 'fluffyunicorn')
        self.other_club = Club.objects.get(name = 'Book Club 2')
        self.url = reverse('create_post', kwargs={'club_id': self.club.id})
        self.other_club_url = reverse('create_post', kwargs={'club_id': self.other_club.id})
        User_Auth.objects.create(user=self.user, rank='owner', club=self.club)
        self.data = {'author': self.user,
                    'text': 'Hi there! I am I unicorn who is very bald',
                    'club': self.club}

    def test_create_post_url(self):
        """Test for the create post url."""

        self.assertEqual(self.url, '/unibook/create-post/1')

    def test_view_posts(self):
        """Test for user being able to view all the posts in the club."""

        url = reverse('club_posts', kwargs={'club_id': self.club.id})
        self.client.login(username=self.user.username, password='Password123')
        self.assertTrue(self._is_logged_in())
        response = self.client.get(url, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_successful_create_post(self):
        """Test for user successfully creating a post."""

        self.client.login(username=self.user.username, password='Password123')
        self.assertTrue(self._is_logged_in())
        post_count_before = Post.objects.count()
        response = self.client.post(self.url, self.data)
        post_count_after = Post.objects.count()
        self.assertEqual(post_count_after, post_count_before+1)
        new_post = Post.objects.latest('created_at')
        self.assertEqual(self.user, new_post.author)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

    def test_unsuccessful_new_post_as_too_long(self):
        """Test user not being able to create a new post because of text being too long."""

        self.client.login(username=self.user.username, password='Password123')
        post_count_before = Post.objects.count()
        self.data['text'] = "x"*281
        response = self.client.post(self.url, self.data)
        post_count_after = Post.objects.count()
        self.assertEqual(post_count_before, post_count_after)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_unsuccessful_new_post_as_blank(self):
        """Test user not being able to create a new post because of blank text."""

        self.client.login(username=self.user.username, password='Password123')
        post_count_before = Post.objects.count()
        self.data['text'] = ""
        response = self.client.post(self.url, self.data)
        post_count_after = Post.objects.count()
        self.assertEqual(post_count_before, post_count_after)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_cannot_create_post_for_other_user(self):
        """Test user not being able to create a post and putting other user as author."""

        self.client.login(username=self.user.username, password='Password123')
        other_user = User.objects.get(username='fluffyunicorn')
        self.data['author'] = other_user.pk
        post_count_before = Post.objects.count()
        response = self.client.post(self.url, self.data)
        post_count_after = Post.objects.count()
        self.assertEqual(post_count_after, post_count_before)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_user_cannot_create_post_for_club_they_are_not_in(self):
        """Test for user not being able to create a post for a club they are not in."""

        self.client.login(username=self.user, password='Password123')
        self.assertTrue(self._is_logged_in())
        self.data['club'] = self.other_club
        response = self.client.post(self.other_club_url, self.data)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
