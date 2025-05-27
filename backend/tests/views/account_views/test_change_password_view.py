""" Unit tests for change password """
from django.contrib.auth.hashers import check_password
from django.urls import reverse
from rest_framework.test import APITestCase
from rest_framework import status
from unibook.tests.helpers import LogInTester
from unibook.models import User, Club, User_Auth

class ChangePasswordTestCase(APITestCase, LogInTester):
    """ Unit tests for change password """

    fixtures = [
        'unibook/tests/fixtures/default_user.json'
    ]

    def setUp(self):
        self.url = reverse('change_password')
        self.user = User.objects.get(username='baldunicorn')
        self.form_input = {
        'old_password':'Password123',
        'new_password':'NewPassword123',
        }

    def test_password_url(self):
        """ Unit tests for change password url """

        self.assertEqual(self.url, '/unibook/change-password/')

    def test_succesful_password_change(self):
        """ Unit tests for successful password change """"

        self.client.login(username=self.user.username, password='Password123')
        self.assertTrue(self._is_logged_in())
        response = self.client.put(self.url, self.form_input)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.user.refresh_from_db()
        is_password_correct = check_password('NewPassword123', self.user.password)
        self.assertTrue(is_password_correct)

    def test_password_change_unsuccesful_without_correct_old_password(self):
        """ Unit tests for unsuccessful password change because old password wrong """

        self.client.login(username=self.user.username, password='Password123')
        self.form_input['old_password'] = 'WrongPassword123'
        response = self.client.put(self.url, self.form_input)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.user.refresh_from_db()
        is_password_correct = check_password('NewPassword123', self.user.password)
        self.assertFalse(is_password_correct)

    def test_unsuccessful_new_password_is_blank(self):
        """ Unit tests for unsuccessful password change because new password is blank """

        self.client.login(username=self.user.username, password='Password123')
        self.assertTrue(self._is_logged_in())
        self.form_input['new_password'] = ''
        response = self.client.put(self.url, self.form_input)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.user.refresh_from_db()
        is_password_correct = check_password('NewPassword123', self.user.password)
        self.assertFalse(is_password_correct)

    def test_unsuccessful_old_password_is_blank(self):
        """ Unit tests for unsuccessful password change because old password is blank """

        self.client.login(username=self.user.username, password='Password123')
        self.assertTrue(self._is_logged_in())
        self.form_input['new_password'] = ''
        response = self.client.put(self.url, self.form_input)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.user.refresh_from_db()
        is_password_correct = check_password('NewPassword123', self.user.password)
        self.assertFalse(is_password_correct)

    def test_get_password_when_not_logged_in_returns_unauthorized(self):
        """ Unit tests for getting change password when not logged in """

        self.assertFalse(self._is_logged_in())
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)
