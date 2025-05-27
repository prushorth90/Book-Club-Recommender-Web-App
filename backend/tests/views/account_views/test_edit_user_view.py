""" Unit test for edit user profile """
from django.contrib.auth.hashers import check_password
from django.urls import reverse
from rest_framework.test import APITestCase
from rest_framework import status
from unibook.models import User
from unibook.tests.helpers import LogInTester

class EditUserTestCase(APITestCase, LogInTester):
    """ Unit test for edit user profile"""

    fixtures = [
        'unibook/tests/fixtures/default_user.json',
        'unibook/tests/fixtures/default_club.json',
        'unibook/tests/fixtures/other_users.json',
        'unibook/tests/fixtures/other_clubs.json'
    ]

    def setUp(self):
        self.user = User.objects.get(username='baldunicorn')
        self.other_user = User.objects.get(username='fluffyunicorn')
        self.url = reverse('edit_user', kwargs={'username': self.user.username})
        self.data = {
            'username': 'unicornbald',
            'email': 'baldy@example.org',
            'first_name': 'Baldyyy',
            'last_name': 'Unikorn',
            'bio': 'I no longer like books.',
            'password': 'Password321'
        }

    def test_edit_user_url(self):
        """ Unit test for edit user url """

        self.assertEqual(self.url, f'/unibook/edit-user/{self.user.username}/')

    def test_user_successfully_editing_user_details(self):
        """ Unit test for successful edit of user detail """

        self.client.login(username=self.user.username, password='Password123')
        self.assertTrue(self._is_logged_in())
        user_count_before = User.objects.count()
        response = self.client.put(self.url, self.data)
        user_count_after = User.objects.count()
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(user_count_before, user_count_after)
        updated_user = User.objects.get(id=self.user.id)
        self.assertEqual(updated_user.username, 'unicornbald')
        self.assertEqual(updated_user.email, 'baldy@example.org')
        self.assertEqual(updated_user.first_name, 'Baldyyy')
        self.assertEqual(updated_user.last_name, 'Unikorn')
        self.assertEqual(updated_user.bio, 'I no longer like books.')
        check_password(updated_user.password, 'Password321')

    def test_user_cannot_edit_another_users_details(self):
        """ Unit test for unsuccessful edit of another user detail """

        self.client.login(username=self.other_user.username, password='Password123')
        self.assertTrue(self._is_logged_in())
        user_count_before = User.objects.count()
        response = self.client.put(self.url, self.data)
        user_count_after = User.objects.count()
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(user_count_before, user_count_after)
        self.assertEqual(self.user.username, 'baldunicorn')
        self.assertEqual(self.user.email, 'baldunicorn@example.org')
        self.assertEqual(self.user.first_name, 'Bald')
        self.assertEqual(self.user.last_name, 'Unicorn')
        self.assertEqual(self.user.bio, 'Books are the best!')

    """ Unit test for username """

    def test_cannot_change_username_to_another_users_username(self):
        self.client.login(username=self.user.username, password='Password123')
        self.assertTrue(self._is_logged_in())
        self.data['username'] = self.other_user.username
        response = self.client.put(self.url, self.data)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(self.user.username, 'baldunicorn')

    def test_cannot_change_username_to_length_over_50(self):
        self.client.login(username=self.user.username, password='Password123')
        self.assertTrue(self._is_logged_in())
        self.data['username'] = 'u'*51
        response = self.client.put(self.url, self.data)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(self.user.username, 'baldunicorn')

    def test_cannot_change_username_to_length_below_3(self):
        self.client.login(username=self.user.username, password='Password123')
        self.assertTrue(self._is_logged_in())
        self.data['username'] = 'u'*2
        response = self.client.put(self.url, self.data)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(self.user.username, 'baldunicorn')

    def test_cannot_change_username_to_blank(self):
        self.client.login(username=self.user.username, password='Password123')
        self.assertTrue(self._is_logged_in())
        self.data['username'] = ''
        response = self.client.put(self.url, self.data)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(self.user.username, 'baldunicorn')

    """ Unit test for email """

    def test_cannot_change_email_to_another_users_email(self):
        self.client.login(username=self.user.username, password='Password123')
        self.assertTrue(self._is_logged_in())
        self.data['email'] = self.other_user.email
        response = self.client.put(self.url, self.data)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(self.user.email, 'baldunicorn@example.org')

    def test_cannot_change_email_to_blank(self):
        self.client.login(username=self.user.username, password='Password123')
        self.assertTrue(self._is_logged_in())
        self.data['email'] = ''
        response = self.client.put(self.url, self.data)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(self.user.email, 'baldunicorn@example.org')

    """ Unit test for first name """

    def test_cannot_change_first_name_to_blank(self):
        self.client.login(username=self.user.username, password='Password123')
        self.assertTrue(self._is_logged_in())
        self.data['first_name'] = ''
        response = self.client.put(self.url, self.data)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(self.user.first_name, 'Bald')

    def test_cannot_change_first_name_to_length_over_50(self):
        self.client.login(username=self.user.username, password='Password123')
        self.assertTrue(self._is_logged_in())
        self.data['first_name'] = 'f'*51
        response = self.client.put(self.url, self.data)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(self.user.first_name, 'Bald')

    def test_can_change_first_name_to_same_name_as_another_user(self):
        self.client.login(username=self.user.username, password='Password123')
        self.assertTrue(self._is_logged_in())
        self.data['first_name'] = self.other_user.first_name
        response = self.client.put(self.url, self.data)
        updated_user = User.objects.get(id=self.user.id)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(updated_user.first_name, self.other_user.first_name)

    """ Unit test for last name """

    def test_cannot_change_last_name_to_blank(self):
        self.client.login(username=self.user.username, password='Password123')
        self.assertTrue(self._is_logged_in())
        self.data['last_name'] = ''
        response = self.client.put(self.url, self.data)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(self.user.last_name, 'Unicorn')

    def test_cannot_change_last_name_to_length_over_50(self):
        self.client.login(username=self.user.username, password='Password123')
        self.assertTrue(self._is_logged_in())
        self.data['last_name'] = 'f'*51
        response = self.client.put(self.url, self.data)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(self.user.last_name, 'Unicorn')

    def test_can_change_last_name_to_same_name_as_another_user(self):
        self.client.login(username=self.user.username, password='Password123')
        self.assertTrue(self._is_logged_in())
        self.data['last_name'] = self.other_user.last_name
        response = self.client.put(self.url, self.data)
        updated_user = User.objects.get(id=self.user.id)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(updated_user.last_name, self.other_user.last_name)

    """ Unit test for bio """

    def test_cannot_change_bio_to_length_over_500(self):
        self.client.login(username=self.user.username, password='Password123')
        self.assertTrue(self._is_logged_in())
        self.data['bio'] = 'b'*501
        response = self.client.put(self.url, self.data)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(self.user.bio, 'Books are the best!')

    def test_can_change_bio_to_blank(self):
        self.client.login(username=self.user.username, password='Password123')
        self.assertTrue(self._is_logged_in())
        self.data['bio'] = ''
        response = self.client.put(self.url, self.data)
        updated_user = User.objects.get(id=self.user.id)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(updated_user.bio, '')

    def test_can_change_bio_to_same_bio_as_other_user(self):
        self.client.login(username=self.user.username, password='Password123')
        self.assertTrue(self._is_logged_in())
        self.data['bio'] = self.other_user.bio
        response = self.client.put(self.url, self.data)
        updated_user = User.objects.get(id=self.user.id)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(updated_user.bio, self.other_user.bio)

    def test_get_edit_user_when_not_logged_in(self):
        """ Test cannot edit user when not logged in"""

        self.assertFalse(self._is_logged_in())
        response = self.client.get(self.url, format='json')
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)
