"""Unit test for remove member """
from unibook.models import User, Club, User_Auth
from unibook.tests.helpers import LogInTester
from django.urls import reverse
from rest_framework.test import APITestCase
from rest_framework import status

class RemoveMemberTestCase(APITestCase, LogInTester):
    """ Unit test for remove member """

    fixtures = [
        'unibook/tests/fixtures/default_user.json',
        'unibook/tests/fixtures/default_club.json',
        'unibook/tests/fixtures/other_users.json',
        'unibook/tests/fixtures/other_clubs.json'
    ]

    def setUp(self):
        self.user = User.objects.get(username='baldunicorn')
        self.other_user = User.objects.get(username='fluffyunicorn')
        self.applicant = User.objects.get(username='user3')
        self.other_user1 = User.objects.get(username='user4')
        self.other_user2 = User.objects.get(username='user5')
        self.club = Club.objects.get(name='Book Club 1')
        self.other_club = Club.objects.get(name='Book Club 2')
        self.owner_auth = User_Auth.objects.create(user=self.user, rank='owner', club=self.club)
        self.member_auth = User_Auth.objects.create(user=self.other_user, rank='member', club=self.club)
        self.applicant_auth = User_Auth.objects.create(user=self.applicant, rank='applicant', club=self.club)
        self.non_member_auth = User_Auth.objects.create(user=self.other_user1, rank='member', club=self.other_club)
        User_Auth.objects.create(user=self.other_user2, rank='owner', club=self.other_club)
        self.applicant_url = reverse('remove_user', kwargs={'auth_id': self.applicant_auth.id})
        self.owner_url = reverse('remove_user', kwargs={'auth_id': self.owner_auth.id})
        self.member_url = reverse('remove_user', kwargs={'auth_id': self.member_auth.id})
        self.non_member_url = reverse('remove_user', kwargs={'auth_id': self.non_member_auth.id})

    def test_remove_user_url(self):
        """ Unit test for removing url """

        self.assertEqual(self.applicant_url, f'/unibook/remove-user/{self.applicant_auth.id}')

    def test_owner_can_reject_applicant(self):
        """ Unit test for owner to reject applicant """

        self.client.login(username=self.user.username, password='Password123')
        self.assertTrue(self._is_logged_in())
        count_before = User_Auth.objects.count()
        response = self.client.delete(self.applicant_url)
        count_after = User_Auth.objects.count()
        self.assertEqual(count_before-1, count_after)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_member_who_is_not_owner_cannot_reject_applicant(self):
        """ Unit test for member who cannot reject applicant """

        self.client.login(username=self.other_user.username, password='Password123')
        self.assertTrue(self._is_logged_in())
        count_before = User_Auth.objects.count()
        response = self.client.delete(self.applicant_url)
        count_after = User_Auth.objects.count()
        self.assertEqual(count_before, count_after)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_applicant_who_is_not_owner_cannot_reject_applicant(self):
        """ Unit test for member who cannot reject applicant """

        self.client.login(username=self.applicant.username, password='Password123')
        self.assertTrue(self._is_logged_in())
        count_before = User_Auth.objects.count()
        response = self.client.delete(self.applicant_url)
        count_after = User_Auth.objects.count()
        self.assertEqual(count_before, count_after)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_user_who_is_not_member_cannot_reject_applicant(self):
        """ Unit test for non club user to reject applicant """

        self.client.login(username=self.other_user1.username, password='Password123')
        self.assertTrue(self._is_logged_in())
        count_before = User_Auth.objects.count()
        response = self.client.delete(self.applicant_url)
        count_after = User_Auth.objects.count()
        self.assertEqual(count_before, count_after)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_owner_cannot_be_removed_from_club(self):
        """ Unit test for owner cannot be removed from club """

        self.client.login(username=self.user.username, password='Password123')
        self.assertTrue(self._is_logged_in())
        count_before = User_Auth.objects.count()
        response = self.client.delete(self.owner_url)
        count_after = User_Auth.objects.count()
        self.assertEqual(count_before, count_after)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_owner_can_remove_member_from_club(self):
        """ Unit test for owner can remove member """

        self.client.login(username=self.user.username, password='Password123')
        self.assertTrue(self._is_logged_in())
        count_before = User_Auth.objects.count()
        response = self.client.delete(self.member_url)
        count_after = User_Auth.objects.count()
        self.assertEqual(count_before-1, count_after)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_owner_cannot_remove_non_member_from_club(self):
        """ Unit test for non member to remove """

        self.client.login(username=self.user.username, password='Password123')
        self.assertTrue(self._is_logged_in())
        count_before = User_Auth.objects.count()
        response = self.client.delete(self.non_member_url)
        count_after = User_Auth.objects.count()
        self.assertEqual(count_before, count_after)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_get_remove_applicant_when_not_logged_in(self):
        """ Test cannot remove applicant when not logged in"""

        self.assertFalse(self._is_logged_in())
        response = self.client.get(self.applicant_url, format='json')
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_get_remove_member_when_not_logged_in(self):
        """ Test cannot remove member when not logged in"""

        self.assertFalse(self._is_logged_in())
        response = self.client.get(self.member_url, format='json')
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_get_remove_non_member_when_not_logged_in(self):
        """ Test cannot remove member when not logged in"""

        self.assertFalse(self._is_logged_in())
        response = self.client.get(self.non_member_url, format='json')
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_get_remove_owner_when_not_logged_in(self):
        """ Test cannot remove member when not logged in"""

        self.assertFalse(self._is_logged_in())
        response = self.client.get(self.owner_url, format='json')
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)
