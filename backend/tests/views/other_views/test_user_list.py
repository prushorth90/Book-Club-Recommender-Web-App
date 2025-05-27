"""Unit tests for the user list view."""
from django.urls import reverse
from unibook.tests.helpers import LogInTester
from unibook.models import User, Club, User_Auth
from rest_framework.test import APITestCase
from rest_framework import status

class TestUserListView(APITestCase, LogInTester):
    """Unit tests for the user list view."""

    fixtures = [
        'unibook/tests/fixtures/default_user.json',
        'unibook/tests/fixtures/other_users.json',
        'unibook/tests/fixtures/default_club.json'
    ]

    def setUp(self):
        self.url = reverse('user_list')
        self.owner = User.objects.get(username='user4')
        self.member = User.objects.get(username='baldunicorn')
        self.applicant = User.objects.get(username='fluffyunicorn')
        self.random_user = User.objects.get(username='user3')
        self.club = Club.objects.get(name='Book Club 1')

        User_Auth.objects.create(
            user=self.owner, rank='owner', club=self.club
        )
        User_Auth.objects.create(
            user=self.member, rank='member', club=self.club
        )
        User_Auth.objects.create(
            user=self.applicant, rank='applicant', club=self.club
        )
        self.form_input = {
            'username': 'harveyelliot',
            'first_name': 'Harvey',
            'last_name': 'Elliot',
            'email': 'harveyelliot@example.org',
            'bio': 'Hi, I am Jon Doe!',
            'password': 'Password123'
        }

    def test_user_list_url(self):
        """Test for the user list url."""

        self.assertEqual(self.url, '/unibook/user-list/')

    def test_get_user_list_redirects_when_not_logged_in(self):
        """Test get redirect when not logged in."""

        self.assertFalse(self._is_logged_in())
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_get_user_list_by_owner(self):
        """Test for owner successfully viewing the member list."""

        self.client.login(username=self.owner.username, password='Password123')
        self.assertTrue(self._is_logged_in())
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_get_user_list_by_member_in_club(self):
        """Test for member successfully viewing the member list."""

        self.client.login(username=self.member.username, password='Password123')
        self.assertTrue(self._is_logged_in())
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
