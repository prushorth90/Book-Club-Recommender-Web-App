""" Unit tests for log out """
from unibook.models import User, Club, User_Auth
from django.urls import reverse
from rest_framework.test import APITestCase
from rest_framework import status
from unibook.tests.helpers import LogInTester

class LogOutTestCase(APITestCase, LogInTester):
    """ Unit tests for log out """

    fixtures = [
        'unibook/tests/fixtures/default_user.json',
        'unibook/tests/fixtures/default_club.json'
    ]

    def setUp(self):
        self.url = reverse('log_out')
        self.user = User.objects.get(username='baldunicorn')

    def test_log_out_url(self):
        """ Unit tests for log out url """

        self.assertEqual(self.url, '/unibook/logout/blacklist/')

    # def test_get_log_out_when_logged_in(self):
    #     """Test for the user successfully logout when logged in."""
    #
    #     self.client.login(username=self.user.username, password='Password123')
    #     self.assertTrue(self._is_logged_in())
    #     response = self.client.get(self.url)
    #     self.assertFalse(self._is_logged_in())
