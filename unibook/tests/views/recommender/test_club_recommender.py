""" Unit test for club recommender view """
from django.urls import reverse
from unibook.models import User, Club, User_Auth
from unibook.tests.helpers import LogInTester
from rest_framework import status
from rest_framework.test import APITestCase

class ClubRecommenderTestCase(APITestCase, LogInTester):
    """ Unit test for club recommender view """

    fixtures = [
        'unibook/tests/fixtures/default_user.json',
        'unibook/tests/fixtures/other_users.json',
        'unibook/tests/fixtures/default_club.json'
    ]

    def setUp(self):
        self.club = Club.objects.get(name='Book Club 1')
        self.user = User.objects.get(username='baldunicorn')
        self.other_user = User.objects.get(username='fluffyunicorn')
        User_Auth.objects.create(user=self.user, rank='member', club=self.club)
        User_Auth.objects.create(user=self.other_user, rank='applicant', club=self.club)
        self.url = reverse('club_recommender', kwargs={'club_id': self.club.id})

    def test_recommender_url(self):
        self.assertEqual(self.url, f'/unibook/club-recommendations/{self.club.id}/')

    def test_logged_out_user_can_not_get_recommended(self):
        """Test that if you are logged out you can not get the recommedner"""

        self.assertFalse(self._is_logged_in())
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_get_club_reccomender(self):
        """Test that if you are part of a club and you are logged in you can get the club recommender"""

        self.client.login(username=self.user.username, password='Password123')
        self.assertTrue(self._is_logged_in())
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
