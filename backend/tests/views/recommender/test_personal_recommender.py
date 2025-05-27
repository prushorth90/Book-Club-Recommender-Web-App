""" Unit test for user recommender view """
from django.urls import reverse
from unibook.models import User
from unibook.tests.helpers import LogInTester
from rest_framework import status
from rest_framework.test import APITestCase

class UserRecommenderViewTestCase(APITestCase, LogInTester):
    """ Unit test for user recommender view """

    fixtures = ['unibook/tests/fixtures/default_user.json']

    def setUp(self):
        self.url = reverse('user_recommender')
        self.user = User.objects.get(username='baldunicorn')

    def test_user_recommender_url(self):
        """Test for user recommender url"""

        self.assertEqual(self.url, '/unibook/user-recommendations/')

    def test_logged_out_user_can_not_get_recommended(self):
        """Test logged out user can not get the recommender"""

        self.assertFalse(self._is_logged_in())
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_get_recommender(self):
        """Test that if you are logged in you can get the recommender"""

        self.client.login(username=self.user.username, password='Password123')
        self.assertTrue(self._is_logged_in())
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
