""" Unit test for book list """
from django.urls import reverse
from django.shortcuts import get_object_or_404
from unibook.models import User, Club, User_Auth, Meeting, BookRating, Book
from unibook.serializers import SignUpSerializer
from unibook.tests.helpers import LogInTester
from rest_framework import status
from rest_framework.test import APITestCase

class BookListTestCase(APITestCase, LogInTester):
    """ Unit test for book list """

    fixtures = [
        'unibook/tests/fixtures/default_user.json',
        'unibook/tests/fixtures/other_users.json',
    ]

    def setUp(self):
        self.url = reverse('book_list')
        self.user = User.objects.get(username='baldunicorn')

    def test_book_list_url(self):
        """ Unit test for book list url """

        self.assertEqual(self.url, '/unibook/book-list/')

    def test_get_book_list(self):
        """ Unit test for get book list """

        self.client.login(username=self.user.username, password="Password123")
        self.assertTrue(self._is_logged_in())
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_get_book_list_when_logged_out_returns_401(self):
        """ Unit test when not logged in to access book list """

        self.assertFalse(self._is_logged_in())
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)
