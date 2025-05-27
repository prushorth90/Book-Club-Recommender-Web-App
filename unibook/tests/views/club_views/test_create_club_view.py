"""Unit tests for create club view."""
from unibook.tests.helpers import LogInTester
from unibook.models import User, Club, User_Auth
from django.urls import reverse
from rest_framework.test import APITestCase
from rest_framework import status
from unibook.tests.helpers import LogInTester

class CreateClubViewTestCase(APITestCase, LogInTester):
    """Unit tests for create club view."""

    fixtures = [
        'unibook/tests/fixtures/default_user.json',
        'unibook/tests/fixtures/default_club.json'
    ]

    def setUp(self):
        self.url = reverse('create_club')
        self.user = User.objects.get(username='baldunicorn')
        self.other_club = Club.objects.get(name='Book Club 1')
        self.form_input = {
            'name': 'Uniclub',
            'description': 'A club for people that falls asleep while reading books.',
            'members_capacity': 50
        }

    def test_create_club_url(self):
        """Test for the create club url."""

        self.assertEqual(self.url, '/unibook/create-club/')

    def test_user_successfully_creating_club(self):
        """Test for the user being able to create a club."""

        self.client.login(username=self.user.username, password='Password123')
        before_count = Club.objects.count()
        response = self.client.post(self.url, self.form_input)
        after_count = Club.objects.count()
        self.assertEqual(after_count, before_count + 1)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        club = Club.objects.get(name='Uniclub')
        self.assertEqual(club.name, 'Uniclub')
        self.assertEqual(club.description, 'A club for people that falls asleep while reading books.')
        self.assertEqual(club.members_capacity, 50)

    def test_unsuccessful_create_club_with_not_unique_name(self):
        """Test for the user not being able to create a club with a name that is not unique."""

        self.client.login(username=self.user.username, password='Password123')
        before_count = Club.objects.count()
        self.form_input['name'] = self.other_club.name
        response = self.client.post(self.url, self.form_input)
        after_count = Club.objects.count()
        self.assertEqual(after_count, before_count)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_unsuccessful_create_club_with_members_capacity_greater_than_50(self):
        """Test for the user not being able to create a club with members capacity greater than 50."""

        self.client.login(username=self.user.username, password='Password123')
        before_count = Club.objects.count()
        self.form_input['members_capacity'] = 51
        response = self.client.post(self.url, self.form_input)
        after_count = Club.objects.count()
        self.assertEqual(after_count, before_count)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_unsuccessful_create_club_with_members_capacity_lesser_than_2(self):
        """Test for the user not being able to create a club with members capacity lesser than 2."""

        self.client.login(username=self.user.username, password='Password123')
        before_count = Club.objects.count()
        self.form_input['members_capacity'] = 1
        response = self.client.post(self.url, self.form_input)
        after_count = Club.objects.count()
        self.assertEqual(after_count, before_count)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_unsuccessful_create_club_with_blank_name(self):
        """Test for the user not being able to create a club with a blank name."""

        self.client.login(username=self.user.username, password='Password123')
        before_count = Club.objects.count()
        self.form_input['name'] = ''
        response = self.client.post(self.url, self.form_input)
        after_count = Club.objects.count()
        self.assertEqual(after_count, before_count)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_unsuccessful_create_club_with_blank_description(self):
        """Test for the user not being able to create a club with a blank description."""

        self.client.login(username=self.user.username, password='Password123')
        before_count = Club.objects.count()
        self.form_input['description'] = ''
        response = self.client.post(self.url, self.form_input)
        after_count = Club.objects.count()
        self.assertEqual(after_count, before_count)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_unsuccessful_create_club_with_name_greater_than_50_characters(self):
        """Test for the user not being able to create a club with a name greater than 50 characters."""

        self.client.login(username=self.user.username, password='Password123')
        before_count = Club.objects.count()
        self.form_input['name'] = 'n' * 51
        response = self.client.post(self.url, self.form_input)
        after_count = Club.objects.count()
        self.assertEqual(after_count, before_count)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_unsuccessful_create_club_with_description_greater_than_500_characters(self):
        """Test for the user not being able to create a club with a blank name."""

        self.client.login(username=self.user.username, password='Password123')
        before_count = Club.objects.count()
        self.form_input['description'] = 'd' * 501
        response = self.client.post(self.url, self.form_input)
        after_count = Club.objects.count()
        self.assertEqual(after_count, before_count)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_unsuccessful_create_club_with_negative_value_for_members_capacity(self):
        """Test for the user not being able to create a club with a negative value for members capacity."""

        self.client.login(username=self.user.username, password='Password123')
        before_count = Club.objects.count()
        self.form_input['members_capacity'] = -1
        response = self.client.post(self.url, self.form_input)
        after_count = Club.objects.count()
        self.assertEqual(after_count, before_count)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_get_create_club_when_not_logged_in(self):
        """ Unit tests to get create club when not logged in """

        self.assertFalse(self._is_logged_in())
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)
