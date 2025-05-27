"""Unit test for other club list view."""
from django.urls import reverse
from unibook.tests.helpers import LogInTester
from unibook.models import User, Club, User_Auth
from rest_framework.test import APITestCase
from rest_framework import status

class OtherClubListViewTestCase(APITestCase, LogInTester):
    """Unit test for other club list view."""

    fixtures = [
        'unibook/tests/fixtures/default_user.json',
        'unibook/tests/fixtures/default_club.json',
        'unibook/tests/fixtures/other_clubs.json'
    ]

    def setUp(self):
        self.user = User.objects.get(username='baldunicorn')
        self.club = Club.objects.get(name='Book Club 1')
        self.other_club = Club.objects.get(name='Book Club 2')
        self.wrong_club = Club.objects.get(name='Book Club 3')
        User_Auth.objects.create(user=self.user, rank='owner', club=self.club)
        User_Auth.objects.create(user=self.user, rank='member', club=self.other_club)
        self.url = reverse('other_club_list')

    def test_other_club_list_url(self):
        """ Test for other club list url """

        self.assertEqual(self.url, '/unibook/other-clubs-list/')

    def test_get_other_club_list(self):
        """ Test to get other club list """

        self.client.login(username=self.user.username, password='Password123')
        self.assertTrue(self._is_logged_in())
        response = self.client.get(self.url, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_successful_display_other_clubs_user_not_in(self):
        """ Test user successfully viewing the clubs the user is not in """

        self.client.login(username=self.user.username, password='Password123')
        self.assertTrue(self._is_logged_in())
        response = self.client.get(self.url, format='json')
        self.assertEqual(1, len(response.data))
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_get_other_club_list_when_not_logged_in(self):
        """ Test to get other club list when not logged in """

        self.assertFalse(self._is_logged_in())
        response = self.client.get(self.url, format='json')
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)
