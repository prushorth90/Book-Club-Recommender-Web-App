""" Unit test for member list view """
from unibook.tests.helpers import LogInTester
from unibook.models import User, Club, User_Auth
from django.urls import reverse
from rest_framework.test import APITestCase
from rest_framework import status

class MemberListTestCase(APITestCase, LogInTester):
    """ Unit test for member list view """

    fixtures = [
        'unibook/tests/fixtures/default_user.json',
        'unibook/tests/fixtures/default_club.json',
    ]

    def setUp(self):
        self.club = Club.objects.get(name='Book Club 1')
        self.url = reverse('member_list', kwargs={'club_id': self.club.id})
        self.user = User.objects.get(username='baldunicorn')
        User_Auth.objects.create(user=self.user, rank='member', club=self.club)


    def test_member_list_url(self):
        """ Unit test for member list url """

        self.assertEqual(self.url, f'/unibook/member-list/{self.club.id}/')

    def test_get_member_list(self):
        """ Unit test to get member list view """

        self.client.login(username=self.user.username, password='Password123')
        self.assertTrue(self._is_logged_in())
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_get_member_list_when_not_logged_in(self):
        """ Unit test to get member list when not logged in """

        self.assertFalse(self._is_logged_in())
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)
