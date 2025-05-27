""" Unit test for leave club view """
from django.core.exceptions import ObjectDoesNotExist
from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase
from unibook.models import User, User_Auth, Club
from unibook.tests.helpers import LogInTester

class LeaveClubViewTestCase(APITestCase, LogInTester):
    """ Unit test for leave club view """

    fixtures = [
        'unibook/tests/fixtures/default_user.json',
        'unibook/tests/fixtures/other_users.json',
        'unibook/tests/fixtures/default_club.json',
        'unibook/tests/fixtures/other_clubs.json'
    ]

    def setUp(self):
        self.owner = User.objects.get(username='baldunicorn')
        self.member = User.objects.get(username='fluffyunicorn')
        self.applicant = User.objects.get(username='user3')
        self.club = Club.objects.get(name='Book Club 1')
        self.wrong_club = Club.objects.get(name='Book Club 2')

        User_Auth.objects.create(user=self.owner, rank='owner', club=self.club)
        User_Auth.objects.create(user=self.member, rank='member', club=self.club)
        User_Auth.objects.create(user=self.applicant, rank='applicant', club=self.club)

        self.url = reverse('leave_club', kwargs={'club_id': self.club.id})

    def test_leave_club_url(self):
        """Test for the leave club url."""

        self.assertEqual(self.url, f'/unibook/leave-club/{self.club.id}/')

    def test_leave_club_when_not_logged_in(self):
        """Test for user not being able to leave a club when not logged in."""

        self.assertFalse(self._is_logged_in())
        response = self.client.delete(self.url, format='json')
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_member_leave_club(self):
        """Test for member successfully leaving a club."""

        self.client.login(username=self.member.username, password='Password123')
        self.assertTrue(self._is_logged_in())
        before_count = User_Auth.objects.count()
        response = self.client.delete(self.url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        after_count = User_Auth.objects.count()
        # Checks if the member has been removed
        self.assertEqual(before_count, after_count + 1)
        # Checks if the member does not exist in the Club
        with self.assertRaises(ObjectDoesNotExist):
            User_Auth.objects.get(user=self.member, club=self.club)

    def test_applicant_leave_club(self):
        """Tests for applicant not being able to leave a club."""

        self.client.login(username=self.applicant.username, password='Password123')
        self.assertTrue(self._is_logged_in())
        before_count = User_Auth.objects.count()
        response = self.client.delete(self.url)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        after_count = User_Auth.objects.count()
        # Checks if no applicant has been removed
        self.assertEqual(before_count, after_count)

        # Checks if the applicant still exists in the Club
        try:
            User_Auth.objects.get(user=self.applicant, club=self.club)
        except (ObjectDoesNotExist):
            self.fail('The user is not allowed to leave the club as applicant')

    def test_owner_leave_club(self):
        """Tests for owner not being able to leave a club."""

        self.client.login(username=self.owner.username, password='Password123')
        self.assertTrue(self._is_logged_in())
        before_count = User_Auth.objects.count()
        response = self.client.delete(self.url)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        after_count = User_Auth.objects.count()
        # Checks if no owner has been removed
        self.assertEqual(before_count, after_count)

        # Checks if the owner still exists in the Club
        try:
            User_Auth.objects.get(user=self.owner, club=self.club)
        except (ObjectDoesNotExist):
            self.fail('The user is not allowed to leave the club as owner')

    """Unit tests for leaving club user is not in"""

    def test_member_leave_wrong_club(self):
        self.client.login(username=self.member.username, password='Password123')
        self.assertTrue(self._is_logged_in())
        self.url = reverse('leave_club', kwargs={'club_id': self.wrong_club.id})
        before_count = User_Auth.objects.count()
        response = self.client.delete(self.url)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        after_count = User_Auth.objects.count()
        # Checks if user_auth count still stays the same
        self.assertEqual(before_count, after_count)

    def test_applicant_leave_wrong_club(self):
        self.client.login(username=self.applicant.username, password='Password123')
        self.assertTrue(self._is_logged_in())
        self.url = reverse('leave_club', kwargs={'club_id': self.wrong_club.id})
        before_count = User_Auth.objects.count()
        response = self.client.delete(self.url)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        after_count = User_Auth.objects.count()
        # Checks if user_auth count still stays the same
        self.assertEqual(before_count, after_count)

    def test_owner_leave_wrong_club(self):
        self.client.login(username=self.owner.username, password='Password123')
        self.assertTrue(self._is_logged_in())
        self.url = reverse('leave_club', kwargs={'club_id': self.wrong_club.id})
        before_count = User_Auth.objects.count()
        response = self.client.delete(self.url)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        after_count = User_Auth.objects.count()
        # Checks if user_auth count still stays the same
        self.assertEqual(before_count, after_count)
