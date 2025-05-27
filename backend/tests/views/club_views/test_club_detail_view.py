""" Unit tests for club detail """
from unibook.tests.helpers import LogInTester
from unibook.models import User, Club, User_Auth
from django.urls import reverse
from rest_framework.test import APITestCase
from rest_framework import status

class ClubDetailsTestCase(APITestCase, LogInTester):
    """ Unit tests for club detail """

    fixtures = [
        'unibook/tests/fixtures/default_user.json',
        'unibook/tests/fixtures/default_club.json'
    ]

    def setUp(self):
        self.other_club = Club.objects.get(name='Book Club 1')
        self.url = reverse('club_detail', kwargs={'club_id': self.other_club.id})
        self.user = User.objects.get(username='baldunicorn')

    def test_club_detail_url(self):
        """ Unit tests for club detail url """

        self.assertEqual(self.url, f'/unibook/club-detail/{self.other_club.id}/')

    def test_get_club_details(self):
        """ Unit tests to get club details """

        self.client.login(username=self.user.username, password = 'Password123')
        self.assertTrue(self._is_logged_in())
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_get_club_details_when_not_logged_in(self):
        """ Unit tests to get club details when not logged in """

        self.assertFalse(self._is_logged_in())
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)
