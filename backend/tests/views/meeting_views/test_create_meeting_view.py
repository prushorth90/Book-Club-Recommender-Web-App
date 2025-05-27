""" Unit test for create meeting view """
from django.urls import reverse
from rest_framework.test import APITestCase
from rest_framework import status
from unibook.models import User, Club, User_Auth, Meeting, Book
from unibook.tests.helpers import LogInTester

class CreateMeetingViewTestCase(APITestCase, LogInTester):
    """ Unit test for create meeting view """

    fixtures = [
        'unibook/tests/fixtures/default_user.json',
        'unibook/tests/fixtures/other_users.json',
        'unibook/tests/fixtures/default_club.json',
        'unibook/tests/fixtures/other_clubs.json',
        'unibook/tests/fixtures/default_book.json'
    ]

    def setUp(self):
        self.owner = User.objects.get(username='baldunicorn')
        self.other_user = User.objects.get(username='fluffyunicorn')
        self.club = Club.objects.get(name='Book Club 1')
        self.other_club = Club.objects.get(name='Book Club 2')
        self.other_club_url = reverse('create_meeting', kwargs={'club_id': self.other_club.id})
        User_Auth.objects.create(user=self.owner, rank='owner', club=self.club)
        User_Auth.objects.create(user=self.other_user, rank='owner', club=self.other_club)
        User_Auth.objects.create(user=self.owner, rank='applicant', club=self.other_club)
        self.book = Book.objects.get(title="Classical Mythology")
        self.form_input = {
            'club' : self.club.pk,
            'creator': self.owner,
            'date': '2029-09-02',
            'time': '09:00',
            'book': self.book.isbn,
            'location': 'Bush House',
            'remote': False,
        }
        self.url = reverse('create_meeting', kwargs={'club_id': self.club.id})

    def test_create_meeting_url(self):
        """ Test for create meeting url"""

        self.assertEqual(self.url, f'/unibook/create-meeting/{self.club.id}/')

    def test_create_meeting_by_owner(self):
        """ Test for owner successfully creating a meeting """

        self.client.login(username=self.owner.username, password='Password123')
        self.assertTrue(self._is_logged_in())
        before_count = Meeting.objects.count()
        response = self.client.post(self.url, self.form_input)
        after_count = Meeting.objects.count()
        self.assertEqual(after_count, before_count + 1)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

    def test_unsuccessful_create_meeting_with_past_date(self):
        """Test for the user not being able to create a meeting with a past date"""

        self.client.login(username=self.owner.username, password='Password123')
        before_count = Meeting.objects.count()
        response = self.client.post(self.url, self.form_input)
        middle_count = Meeting.objects.count()
        self.assertEqual(middle_count, before_count + 1)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        form_input2 = {
            'date': '2000-09-02',
            'time': '09:00',
            'book': 'Jack Potter',
            'location': 'Hogwart'
        }
        response2 = self.client.post(self.url, form_input2)
        after_count = Meeting.objects.count()
        self.assertEqual(after_count, middle_count)
        self.assertEqual(response2.status_code, status.HTTP_400_BAD_REQUEST)

    def test_create_meeting_with_blank_time_returns_bad_request(self):
        """Test user not being able to create a meeting if time is blank."""

        self.client.login(username=self.owner.username, password='Password123')
        self.assertTrue(self._is_logged_in())
        self.form_input['time'] = ''
        response = self.client.post(self.url, self.form_input)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_create_meeting_with_blank_location_returns_bad_request(self):
        """Test user not being able to create a meeting if location is blank."""

        self.client.login(username=self.owner.username, password='Password123')
        self.assertTrue(self._is_logged_in())
        self.form_input['location'] = ''
        response = self.client.post(self.url, self.form_input)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_user_cannot_create_meeting_for_club_they_are_not_in(self):
        """Test user not being able to create a meeting for club user is not in."""

        self.client.login(username=self.owner.username, password='Password123')
        self.assertTrue(self._is_logged_in())
        self.form_input['club'] = self.other_club
        response = self.client.post(self.other_club_url, self.form_input)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_get_create_meeting_when_not_logged_in(self):
        """ Test cannot create meeting when not logged in"""

        self.assertFalse(self._is_logged_in())
        response = self.client.get(self.url, format='json')
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)
