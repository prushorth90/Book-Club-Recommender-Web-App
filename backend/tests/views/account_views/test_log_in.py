"""Unit tests of the log in."""
from unibook.models import User
from unibook.tests.helpers import LogInTester
from django.urls import reverse
from rest_framework.test import APITestCase
from rest_framework import status

class LogInTestCase(APITestCase, LogInTester):
    """Unit tests of the log in."""

    fixtures = ['unibook/tests/fixtures/default_user.json']

    def setUp(self):
        self.url = reverse('token_obtain_pair')
        self.user = User.objects.get(username='baldunicorn')
        self.user_input = {'username': 'baldunicorn', 'password': 'Password123'}

    def test_log_in_url(self):
        """"Test for the log in url."""

        self.assertEqual(self.url, '/unibook/token/obtain/')

    def test_unsuccessful_log_in(self):
        """Test for unsuccessful log in with incorrect password."""

        self.user_input['password'] = 'wrongpassword'
        response = self.client.post(self.url, self.user_input)
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)
        self.assertFalse(self._is_logged_in())

    def test_successful_user_log_in(self):
        """Test for successful log in with correct credentials."""

        self.user.is_active=True
        response = self.client.post(self.url, self.user_input, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    # def test_post_log_in_view_when_logged_in(self):
    #     """Test user not being able to post input to the log in view if user is logged in."""
    #
    #     self.client.login(email=self.user.email, password="Password123")
    #     self.assertTrue(self._is_logged_in())
    #     response = self.client.post(self.url, self.user_input)
    #     self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
    #     self.assertTrue(self._is_logged_in())

    def test_log_in_with_blank_username(self):
        """Test user not being able to log in if user enter a blank username."""

        self.user_input['username'] = ''
        response = self.client.post(self.url, self.user_input)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_log_in_with_blank_password(self):
        """Test user not being able to log in if user enter a blank password."""

        self.user_input['password'] = ''
        response = self.client.post(self.url, self.user_input)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
