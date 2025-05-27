""" Unit tests for delete club view """
from unibook.models import User, Club, User_Auth
from django.urls import reverse
from rest_framework.test import APITestCase
from rest_framework import status
from unibook.tests.helpers import LogInTester

class DeleteClubTestCase(APITestCase, LogInTester):
    """ Unit tests for delete club view """

    fixtures = [
        'unibook/tests/fixtures/default_user.json',
        'unibook/tests/fixtures/other_users.json',
        'unibook/tests/fixtures/default_club.json'
    ]

    def setUp(self):
        self.club = Club.objects.get(name='Book Club 1')
        self.user = User.objects.get(username='baldunicorn')
        self.other_user = User.objects.get(username='fluffyunicorn')
        self.other_user1 = User.objects.get(username='user3')
        User_Auth.objects.create(user=self.user, rank='owner', club=self.club)
        User_Auth.objects.create(user=self.other_user, rank='member', club=self.club)
        User_Auth.objects.create(user=self.other_user1, rank='applicant', club=self.club)
        self.url = reverse('delete_club',kwargs={'club_id': self.club.id})

    def test_delete_club_url(self):
        """ Unit tests for delete club url """

        self.assertEqual(self.url, f'/unibook/delete-club/{self.club.id}/')

    def test_owner_can_delete_club(self):
        """ Unit tests for owner to delete club """

        self.client.login(username=self.user.username, password='Password123')
        self.assertTrue(self._is_logged_in())
        club_count_before = Club.objects.count()
        response = self.client.delete(self.url)
        club_count_after = Club.objects.count()
        self.assertEqual(club_count_before-1, club_count_after)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_applicant_who_is_not_owner_cannot_delete_club(self):
        """ Unit tests for member who cannot delete club """

        self.client.login(username=self.other_user1.username, password='Password123')
        self.assertTrue(self._is_logged_in())
        club_count_before = Club.objects.count()
        response = self.client.delete(self.url)
        club_count_after = Club.objects.count()
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(club_count_before, club_count_after)

    def test_member_who_is_not_owner_cannot_delete_club(self):
        """ Unit tests for member who cannot delete club """

        self.client.login(username=self.other_user.username, password='Password123')
        self.assertTrue(self._is_logged_in())
        club_count_before = Club.objects.count()
        response = self.client.delete(self.url)
        club_count_after = Club.objects.count()
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(club_count_before, club_count_after)

    def test_user_who_is_not_member_cannot_delete_club(self):
        """ Unit test for non-club user to try to delete club """

        self.client.login(username=self.other_user1.username, password='Password123')
        self.assertTrue(self._is_logged_in())
        club_count_before = Club.objects.count()
        response = self.client.delete(self.url)
        club_count_after = Club.objects.count()
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(club_count_before, club_count_after)

    def test_get_delete_club_when_not_logged_in(self):
        """ Test cannot delete club when not logged in"""

        self.assertFalse(self._is_logged_in())
        response = self.client.get(self.url, format='json')
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)
