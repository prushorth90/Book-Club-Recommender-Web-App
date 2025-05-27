"""Unit tests for user detail view."""
from django.urls import reverse
from unibook.tests.helpers import LogInTester
from unibook.models import User, Club, User_Auth
from rest_framework.test import APITestCase
from rest_framework import status

class UserDetailsTestCase(APITestCase, LogInTester):
    """Unit tests for user detail view."""

    fixtures = [
        'unibook/tests/fixtures/default_user.json',
        'unibook/tests/fixtures/default_club.json'
    ]

    def setUp(self):
        self.other_club = Club.objects.get(name='Book Club 1')
        self.user = User.objects.get(username='baldunicorn')
        self.url = reverse('user_detail', kwargs={'username': self.user.username})

    def test_club_detail_url(self):
        """Test for the club detail view url."""

        self.assertEqual(self.url, f'/unibook/user-detail/{self.user.username}/')

    def test_get_club_details_when_logged_in(self):
        """Test get the user details when logged in is all good"""

        self.client.login(username=self.user.username, password='Password123')
        self.assertTrue(self._is_logged_in())
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_get_club_details_when_logged_out(self):
        """Test you can not get user details view when you're logged out"""

        self.assertFalse(self._is_logged_in())
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)
