""" Unit test for applicant list view """
from unibook.tests.helpers import LogInTester
from unibook.models import User, Club, User_Auth
from django.urls import reverse
from rest_framework.test import APITestCase
from rest_framework import status

class ApplicantListTestCase(APITestCase, LogInTester):
    """ Unit test for applicant list view """

    fixtures = [
        'unibook/tests/fixtures/default_user.json',
        'unibook/tests/fixtures/default_club.json'
    ]

    def setUp(self):
        self.club = Club.objects.get(name='Book Club 1')
        self.url = reverse('applicant_list', kwargs={'club_id': self.club.id})
        self.user = User.objects.get(username='baldunicorn')

    def test_applicant_list_url(self):
        """ Unit test for applicant list url """

        self.assertEqual(self.url, f'/unibook/applicant-list/{self.club.id}/')

    def test_get_applicant_list(self):
        """ Unit test to get applicant list view """

        self.client.login(username=self.user.username, password='Password123')
        self.assertTrue(self._is_logged_in())
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_get_applicant_list_when_not_logged_in(self):
        """ Unit test to get applicant list when not logged in """

        self.assertFalse(self._is_logged_in())
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)
