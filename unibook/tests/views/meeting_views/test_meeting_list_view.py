"""Unit tests for meeting list view"""
from unibook.models import User, User_Auth, Club
from django.urls import reverse
from unibook.tests.helpers import LogInTester
from rest_framework import status
from rest_framework.test import APITestCase

class MeetingListViewTestCase(APITestCase, LogInTester):
    """Unit tests for meeting list view"""

    fixtures = [
        'unibook/tests/fixtures/default_user.json',
        'unibook/tests/fixtures/other_users.json',
        'unibook/tests/fixtures/default_club.json'
    ]

    def setUp(self):
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

        self.url = reverse('meeting_list', kwargs={'club_id': self.club.id})

    def test_meeting_list_url(self):
        """Test for the meeting_list url"""

        self.assertEqual(self.url, f'/unibook/meeting-list/{self.club.id}/')

    def test_get_meeting_list_when_not_logged_in(self):
        """ Test user not being able to view the meetings when not logged in"""

        self.assertFalse(self._is_logged_in())
        response = self.client.get(self.url, format='json')
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_get_meeting_list_by_owner(self):
        """Test for owner successfully viewing the club meetings."""

        self.client.login(username=self.owner.username, password='Password123')
        self.assertTrue(self._is_logged_in())
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_get_meeting_list_by_member_in_club(self):
        """Test for member successfully viewing the club meetings."""

        self.client.login(username=self.member.username, password='Password123')
        self.assertTrue(self._is_logged_in())
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    #UNCOMMENT WHEN PERMISSIONS ARE ADDED
    # def test_get_meeting_list_by_applicant(self):
    #     """Test for applicant not being able to view the club meetings."""
    #
    #     self.client.login(username=self.applicant.username, password='Password123')
    #     self.assertTrue(self._is_logged_in())
    #     response = self.client.get(self.url)
    #     self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
    #
    # def test_get_meeting_list_by_user_not_in_club(self):
    #     """Test for user not in the club not being able to view the club meetings."""
    #
    #     self.client.login(username=self.random_user.username, password='Password123')
    #     self.assertTrue(self._is_logged_in())
    #     response = self.client.get(self.url)
    #     self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
