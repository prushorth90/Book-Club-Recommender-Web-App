"""Unit tests for the owner list view."""
from django.urls import reverse
from unibook.tests.helpers import LogInTester
from unibook.models import User, Club, User_Auth
from rest_framework.test import APITestCase
from rest_framework import status

class OwnerListTestCase(APITestCase, LogInTester):
    """Unit tests for the owner list view."""

    fixtures = [
        'unibook/tests/fixtures/default_user.json',
        'unibook/tests/fixtures/default_club.json'
    ]

    def setUp(self):
        self.club = Club.objects.get(name='Book Club 1')
        self.url = reverse('owner_list', kwargs={'club_id': self.club.id})
        self.user = User.objects.get(username='baldunicorn')
        User_Auth.objects.create(user=self.user, rank='owner', club=self.club)

    def test_owner_list_url(self):
        """Test for the owner list url."""

        self.assertEqual(self.url, f'/unibook/owner-list/{self.club.id}/')

    def test_get_owner_list(self):
        """Test owner successfully getting the owner list view."""

        self.client.login(username=self.user.username, password='Password123')
        self.assertTrue(self._is_logged_in())
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_get_owner_list_when_not_logged_in(self):
        """Test user not being able to get an owner list when not logged in."""

        self.assertFalse(self._is_logged_in())
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)
