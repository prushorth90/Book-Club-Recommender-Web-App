"""Unit tests for current user view."""
from django.urls import reverse
from rest_framework.test import APITestCase
from rest_framework import status
from unibook.models import User, Club, User_Auth
from unibook.tests.helpers import LogInTester

class CurrentUserViewTestCase(APITestCase, LogInTester):
    """Unit tests for current user view."""

    fixtures = [
        'unibook/tests/fixtures/default_user.json',
        'unibook/tests/fixtures/default_club.json'
    ]

    def setUp(self):
        self.user = User.objects.get(username='baldunicorn')
        self.url = reverse('current_user')
        self.club = Club.objects.get(name='Book Club 1')

    def test_current_user_url(self):
        """Test for the current user view url."""

        self.assertEqual(self.url, '/unibook/current-user/')

    def test_get_current_user_when_logged_in(self):
        """Test get the current user when logged in is all good"""

        self.client.login(username=self.user.username, password='Password123')
        self.assertTrue(self._is_logged_in())
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_get_current_user_when_logged_out(self):
        """Test you can not get current user view when you're logged out"""

        self.assertFalse(self._is_logged_in())
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)
