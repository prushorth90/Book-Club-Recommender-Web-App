""" Unit tests for accepting an applicant """
from unibook.models import User, Club, User_Auth
from django.urls import reverse
from rest_framework.test import APITestCase
from rest_framework import status
from unibook.tests.helpers import LogInTester

class AcceptApplicantTestCase(APITestCase, LogInTester):
    """ Unit tests for accepting an applicant """

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
        self.club = Club.objects.get(name='Book Club 1')
        User_Auth.objects.create(user=self.user, rank='owner', club=self.club)
        User_Auth.objects.create(user=self.other_user, rank='member', club=self.club)
        self.auth = User_Auth.objects.create(user=self.applicant, rank='applicant', club=self.club)
        self.url = reverse('accept_user', kwargs={'auth_id': self.auth.id})
        self.data = {
            'rank': 'member',
            'club': self.club,
            'user': self.applicant
        }

    def test_accept_applicant_url(self):
        """ Unit tests for accept applicant url """

        self.assertEqual(self.url, f'/unibook/accept-user/{self.auth.id}/')

    def test_owner_can_accept_applicant(self):
        """ Unit tests for owner accepting applicant """

        self.client.login(username=self.user.username, password='Password123')
        self.assertTrue(self._is_logged_in())
        count_before = User_Auth.objects.count()
        response = self.client.put(self.url)
        count_after = User_Auth.objects.count()
        updated = User_Auth.objects.get(id=self.auth.id)
        self.assertEqual(count_before, count_after)
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertEqual(updated.rank, 'member')
        self.assertEqual(updated.user, self.applicant)

    def test_member_who_is_not_owner_cannot_accept_applicant(self):
        """ Unit tests for members who cannot accept applcaint """

        self.client.login(username=self.other_user.username, password='Password123')
        self.assertTrue(self._is_logged_in())
        count_before = User_Auth.objects.count()
        response = self.client.put(self.url)
        count_after = User_Auth.objects.count()
        self.assertEqual(count_before, count_after)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_user_who_is_not_member_cannot_accept_applicant(self):
        """ Unit tests for user not in club cannot accept applicant """

        self.client.login(username=self.other_user1.username, password='Password123')
        self.assertTrue(self._is_logged_in())
        count_before = User_Auth.objects.count()
        response = self.client.put(self.url)
        count_after = User_Auth.objects.count()
        self.assertEqual(count_before, count_after)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)


    def test_get_accept_applicant_when_not_logged_in(self):
        """ Test cannot accept applicant when not logged in"""

        self.assertFalse(self._is_logged_in())
        response = self.client.get(self.url, format='json')
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)
