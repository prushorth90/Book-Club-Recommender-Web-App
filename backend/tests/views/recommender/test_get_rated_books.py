""" Unit test for get rated book """
from django.urls import reverse
from unibook.models import User
from unibook.tests.helpers import LogInTester
from rest_framework import status
from rest_framework.test import APITestCase

class GetRatedBooksTestCase(APITestCase, LogInTester):
    """ Unit test for get rated book """

    fixtures = ['unibook/tests/fixtures/default_user.json']

    def setUp(self):
        self.user = User.objects.get(username='baldunicorn')
        self.url = reverse('get_rated_book')

    def test_get_rated_books_url(self):
        """Test for rated books url"""

        self.assertEqual(self.url, '/unibook/get_rated_books/')

    def test_get_rated_books_when_logged_in_returns_200(self):
        """Test you can get the books if you are logged in"""

        self.client.login(username=self.user.username, password='Password123')
        self.assertTrue(self._is_logged_in())
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_get_rated_books_when_logged_out_returns_unauthorized(self):
        """Test you can not get the books if you are logged out"""

        self.assertFalse(self._is_logged_in())
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)
