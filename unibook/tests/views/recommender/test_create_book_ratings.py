""" Unit test for create book rating """
from django.urls import reverse
from unibook.models import User, Book
from unibook.tests.helpers import LogInTester
from rest_framework import status
from rest_framework.test import APITestCase
import pandas as pd

class CreateBookRatingsTestCase(APITestCase, LogInTester):
    """ Unit test for create book rating """

    fixtures = [
        'unibook/tests/fixtures/other_users.json',
        'unibook/tests/fixtures/default_book.json',
    ]

    def setUp(self):
        self.url = reverse('book_ratings')
        self.user = User.objects.get(username='user6')
        self.book = Book.objects.get(isbn= "0195153448")
        self.form_input = {
        'book' : self.book.isbn,
        'rating': 8,
        }
        self.ratings_path = 'unibook/recommender/book_dataset/BX_Book_Ratings.csv'

    def test_create_book_ratings_url(self):
        """ Unit test for create book url """

        self.assertEqual(self.url, '/unibook/book_rating/')

    def test_can_create_ratings_when_logged_in(self):
        """ Unit test for post create rating form """

        self.client.login(username=self.user.username, password='Password123')
        self.assertTrue(self._is_logged_in())
        response = self.client.post(self.url, self.form_input)
        books = pd.read_csv(self.ratings_path, sep=';', encoding='ISO-8859-1')
        books = books.drop(books.tail(1).index)
        books.to_csv(self.ratings_path, sep=';',encoding='ISO-8859-1', index=False)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    """ Unit test for rating boundary """

    def test_rating_has_to_be_less_than_11(self):
        self.client.login(username=self.user.username, password='Password123')
        self.assertTrue(self._is_logged_in())
        self.form_input['rating'] = 11
        response = self.client.post(self.url, self.form_input)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_rating_has_to_be_more_than_1(self):
        self.client.login(username=self.user.username, password='Password123')
        self.assertTrue(self._is_logged_in())
        self.form_input['rating'] = 0
        response = self.client.post(self.url, self.form_input)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_rating_can_not_be_negative(self):
        self.client.login(username=self.user.username, password='Password123')
        self.assertTrue(self._is_logged_in())
        self.form_input['rating'] = -1
        response = self.client.post(self.url, self.form_input)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_can_not_create_ratings_when_logged_out(self):
        """ Test cannot access form when not logged in """

        self.assertFalse(self._is_logged_in())
        response = self.client.post(self.url, self.form_input)
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)
