""" Unit test for edit club detail """
from unibook.tests.helpers import LogInTester
from unibook.models import User, Club, User_Auth
from django.urls import reverse
from rest_framework.test import APITestCase
from rest_framework import status

class EditClubViewTestCase(APITestCase, LogInTester):
    """ Unit test for edit club detail """

    fixtures = [
        'unibook/tests/fixtures/default_user.json',
        'unibook/tests/fixtures/default_club.json',
        'unibook/tests/fixtures/other_users.json',
        'unibook/tests/fixtures/other_clubs.json'
    ]

    def setUp(self):
        self.user = User.objects.get(username='baldunicorn')
        self.other_user = User.objects.get(username='fluffyunicorn')
        self.other_user1 = User.objects.get(username='user3')
        self.club = Club.objects.get(name='Book Club 1')
        self.other_club = Club.objects.get(name='Book Club 2')
        User_Auth.objects.create(user=self.user, rank='owner', club=self.club)
        User_Auth.objects.create(user=self.other_user, rank='member', club=self.club)
        self.url = reverse('edit_club', kwargs={'club_id': self.club.id})
        self.form_input = {
        'name': 'Uniclub',
        'description': 'A club for people that fall asleep while reading books.',
        'members_capacity': 34
        }

    def test_edit_club_url(self):
        self.assertEqual(self.url, f'/unibook/edit-club/{self.club.id}/')

    def test_user_successfully_editing_club(self):
        """Test for the user being able to edit a club."""

        self.client.login(username=self.user.username, password='Password123')
        self.assertTrue(self._is_logged_in())
        club_count_before = Club.objects.count()
        response = self.client.put(self.url, self.form_input)
        club_count_after = Club.objects.count()
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertEqual(club_count_before, club_count_after)
        # Test if the club information is correct
        club = Club.objects.get(id=self.club.id)
        self.assertEqual(club.name, 'Uniclub')
        self.assertEqual(club.description, 'A club for people that fall asleep while reading books.')
        self.assertEqual(club.members_capacity, 34)


    def test_member_who_is_not_owner_cannot_edit_club(self):
        """Test for the member who cannot edit club."""

        self.client.login(username=self.other_user.username, password='Password123')
        self.assertTrue(self._is_logged_in())
        response = self.client.put(self.url, self.form_input)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertNotEqual(self.club.name, 'Uniclub')
        self.assertNotEqual(self.club.description, 'A club for people that fall asleep while reading books.')
        self.assertNotEqual(self.club.members_capacity, 34)

    def test_user_who_is_not_member_cannot_edit_club(self):
        """Test for the user who cannot edit club."""

        self.client.login(username=self.other_user1.username, password='Password123')
        self.assertTrue(self._is_logged_in())
        response = self.client.put(self.url, self.form_input)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertNotEqual(self.club.name, 'Uniclub')
        self.assertNotEqual(self.club.description, 'A club for people that fall asleep while reading books.')
        self.assertNotEqual(self.club.members_capacity, 34)

    def test_unsuccessful_create_club_with_not_unique_name(self):
        """Test for the user not being able to edit a club with a name that is not unique."""

        self.client.login(username=self.user.username, password='Password123')
        self.assertTrue(self._is_logged_in())
        self.form_input['name'] = 'Book Club 2'
        response = self.client.put(self.url, self.form_input)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertNotEqual('Book Club 2', self.club.name)
        self.assertEqual('Book Club 1', self.club.name)

    def test_unsuccessful_edit_club_with_members_capacity_greater_than_50(self):
        """Test for the user not being able to edit a club with members capacity greater than 50."""

        self.client.login(username=self.user.username, password='Password123')
        self.assertTrue(self._is_logged_in())
        self.form_input['members_capacity'] = 51
        response = self.client.put(self.url, self.form_input)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertNotEqual(self.club.members_capacity, 51)
        self.assertEqual(self.club.members_capacity, 10)

    def test_unsuccessful_edit_club_with_members_capacity_lesser_than_2(self):
        """Test for the user not being able to edit a club with members capacity lesser than 2."""

        self.client.login(username=self.user.username, password='Password123')
        self.assertTrue(self._is_logged_in())
        self.form_input['members_capacity'] = 1
        response = self.client.put(self.url, self.form_input)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertNotEqual(self.club.members_capacity, 1)
        self.assertEqual(self.club.members_capacity, 10)

    def test_unsuccessful_edit_club_with_blank_name(self):
        """Test for the user not being able to edit a club with a blank name."""

        self.client.login(username=self.user.username, password='Password123')
        self.assertTrue(self._is_logged_in())
        self.form_input['name'] = ''
        response = self.client.put(self.url, self.form_input)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(self.club.name, 'Book Club 1')

    def test_unsuccessful_edit_club_with_blank_description(self):
        """Test for the user not being able to create a club with a blank description."""

        self.client.login(username=self.user.username, password='Password123')
        self.assertTrue(self._is_logged_in())
        self.form_input['description'] = ''
        response = self.client.put(self.url, self.form_input)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(self.club.description, 'This is a book club')

    def test_unsuccessful_edit_club_with_name_greater_than_50_characters(self):
        """Test for the user not being able to edit a club with a name greater than 50 characters."""

        self.client.login(username=self.user.username, password='Password123')
        self.assertTrue(self._is_logged_in())
        self.form_input['name'] = 'n' * 51
        response = self.client.put(self.url, self.form_input)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertNotEqual(self.club.name, 'n'*51)
        self.assertEqual(self.club.name, 'Book Club 1')

    def test_unsuccessful_edit_club_with_description_greater_than_500_characters(self):
        """Test for the user not being able to edit a club with a too long description"""

        self.client.login(username=self.user.username, password='Password123')
        self.assertTrue(self._is_logged_in())
        self.form_input['description'] = 'd' * 501
        response = self.client.put(self.url, self.form_input)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertNotEqual(self.club.description, 'd'*501)
        self.assertEqual(self.club.description, 'This is a book club')

    def test_unsuccessful_edit_club_with_negative_value_for_members_capacity(self):
        """Test for the user not being able to edit a club with a negative value for members capacity."""

        self.client.login(username=self.user.username, password='Password123')
        self.form_input['members_capacity'] = -1
        response = self.client.put(self.url, self.form_input)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertNotEqual(self.club.members_capacity, -1)
        self.assertEqual(self.club.members_capacity, 10)


    def test_get_edit_club_when_not_logged_in(self):
        """ Test cannot edit club when not logged in"""

        self.assertFalse(self._is_logged_in())
        response = self.client.get(self.url, format='json')
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)
