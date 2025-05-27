""" Unit test for sign up """
from unibook.models import User
from django.urls import reverse
from rest_framework.test import APITestCase
from rest_framework import status
from unibook.tests.helpers import LogInTester

class SignUpViewTestCase(APITestCase, LogInTester):
    """ Tests for sign up view """

    fixtures = ['unibook/tests/fixtures/default_user.json']

    def setUp(self):
        self.url = reverse('signup')
        self.form_input = {
            'username': 'harveyelliot',
            'first_name': 'Harvey',
            'last_name': 'Elliot',
            'email': 'harveyelliot@example.org',
            'bio': 'Hi, I am Jon Doe!',
            'password': 'Password123',
        }
        self.user = User.objects.get(username='baldunicorn')

    def test_sign_up_url(self):
        """ Unit test for url """

        self.assertEqual(self.url, '/unibook/signup/')

    def test_succesful_sign_up_creates_new_user(self):
        """ Unit test for creating new user """

        self.assertFalse(self._is_logged_in())
        before_count = User.objects.count()
        response = self.client.post(self.url, self.form_input)
        after_count = User.objects.count()
        self.assertEqual(after_count, before_count + 1)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

    """ Unit tests for blank name """

    def test_sign_up_with_blank_first_name_returns_bad_request(self):
        self.assertFalse(self._is_logged_in())
        self.form_input['first_name'] = ''
        response = self.client.post(self.url, self.form_input)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_sign_up_with_blank_last_name_returns_bad_request(self):
        self.assertFalse(self._is_logged_in())
        self.form_input['last_name'] = ''
        response = self.client.post(self.url, self.form_input)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    """ Unit tests for non unique name """

    def test_sign_up_with_non_unique_first_name_returns_201_created(self):
        self.assertFalse(self._is_logged_in())
        self.form_input['first_name'] = self.user.first_name
        response = self.client.post(self.url, self.form_input)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

    def test_sign_up_with_non_unique_last_name_returns_201_created(self):
        self.assertFalse(self._is_logged_in())
        self.form_input['last_name'] = self.user.last_name
        response = self.client.post(self.url, self.form_input)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

    """ Unit test for email """

    def test_sign_up_with_blank_email_returns_bad_request(self):
        self.assertFalse(self._is_logged_in())
        self.form_input['email'] = ''
        response = self.client.post(self.url, self.form_input)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_sign_up_with_not_unique_email_does_not_create_new_user_and_returns_bad_request(self):
        self.assertFalse(self._is_logged_in())
        before = User.objects.count()
        self.form_input['email'] = self.user.email
        response = self.client.post(self.url, self.form_input)
        after = User.objects.count()
        self.assertEqual(after, before)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    """ Unit test for username """

    def test_sign_up_with_blank_username_returns_bad_request(self):
        self.assertFalse(self._is_logged_in())
        self.form_input['username'] = ''
        response = self.client.post(self.url, self.form_input)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_sign_up_with_not_unique_username_does_not_create_new_user_and_returns_bad_request(self):
        self.assertFalse(self._is_logged_in())
        before_count = User.objects.count()
        input = self.form_input
        input['username'] = self.user.username
        response = self.client.post(self.url, input)
        after_count = User.objects.count()
        self.assertEqual(after_count, before_count)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_sign_up_with_blank_password_returns_bad_request(self):
        """ Unit test for password """

        self.assertFalse(self._is_logged_in())
        self.form_input['password'] = ''
        response = self.client.post(self.url, self.form_input)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    """ Unit test for bio """

    def test_sign_up_with_non_unique_bio_returns_201_created(self):
        self.assertFalse(self._is_logged_in())
        self.form_input['bio'] = self.user.bio
        response = self.client.post(self.url, self.form_input)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

    def test_sign_up_with_blank_bio_returns_201_created(self):
        self.assertFalse(self._is_logged_in())
        self.form_input['bio'] = ''
        response = self.client.post(self.url, self.form_input)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
