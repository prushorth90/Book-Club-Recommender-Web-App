"""Unit tests for create user auth view."""
from django.urls import reverse
from rest_framework.test import APITestCase
from rest_framework import status
from unibook.models import User, Club, User_Auth
from unibook.tests.helpers import LogInTester

class CreateUserAuthViewTestCase(APITestCase, LogInTester):
    """Unit tests for create user auth view."""

    fixtures = [
        'unibook/tests/fixtures/default_user.json',
        'unibook/tests/fixtures/default_club.json'
    ]

    def setUp(self):
        self.url = reverse('create_user_auth')
        self.other_club = Club.objects.get(name='Book Club 1')
        self.user = User.objects.get(username='baldunicorn')
        self.form_input = {
            'rank': 'member',
            'club': self.other_club,
            'user': self.user
        }

    def test_create_user_auth_url(self):
        """Test for create user auth url."""

        self.assertEqual(self.url, '/unibook/create-user-auth/')

    def test_post_create_user_auth(self):
        """Test successful create user auth."""

        self.client.login(username=self.user.username, password='Password123')
        self.assertTrue(self._is_logged_in())
        response = self.client.post(self.url, self.form_input)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

    def test_club_can_not_be_blank(self):
        """Test unsuccessful create user auth if club is blank."""

        self.client.login(username=self.user.username, password='Password123')
        self.assertTrue(self._is_logged_in())
        self.form_input['club'] = ''
        response = self.client.post(self.url, self.form_input)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_user_can_not_be_blank(self):
        """Test unsuccessful create user auth if user is blank."""

        self.client.login(username=self.user.username, password='Password123')
        self.assertTrue(self._is_logged_in())
        self.form_input['user'] = ''
        response = self.client.post(self.url, self.form_input)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_rank_has_to_be_one_of_the_choices(self):
        """Test successful create user auth if rank is from the choices."""

        self.client.login(username=self.user.username, password='Password123')
        self.assertTrue(self._is_logged_in())
        self.form_input['rank'] = 'member' or 'applicant' or 'owner'
        response = self.client.post(self.url, self.form_input)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

    def test_rank_can_not_be_outside_of_the_choices(self):
        """Test unsuccessful create user auth if rank is not from the choices."""

        self.client.login(username=self.user.username, password='Password123')
        self.assertTrue(self._is_logged_in())
        self.form_input['rank'] = 'officer'
        response = self.client.post(self.url, self.form_input)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_rank_has_max_length_of_9_charcaters(self):
        """Test unsuccessful create user auth if rank is greater than 9 characters."""

        self.client.login(username=self.user.username, password='Password123')
        self.assertTrue(self._is_logged_in())
        self.form_input['rank'] = 'm' * 10
        response = self.client.post(self.url, self.form_input)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_cannot_create_2_objects_for_same_user_and_club(self):
        """Test unsuccessful create user auth for same user and club."""

        self.client.login(username=self.user.username, password='Password123')
        self.assertTrue(self._is_logged_in())
        before_count = User_Auth.objects.count()
        response = self.client.post(self.url, self.form_input)
        middle_count = User_Auth.objects.count()
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(before_count+1, middle_count)
        response = self.client.post(self.url, self.form_input)
        after_count = User_Auth.objects.count()
        self.assertEqual(middle_count, after_count)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
