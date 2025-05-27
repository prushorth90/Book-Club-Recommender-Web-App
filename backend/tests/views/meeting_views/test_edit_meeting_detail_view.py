""" Unit test for edit a meeting """
from django.urls import reverse
from rest_framework.test import APITestCase
from rest_framework import status
from unibook.models import User, Club, User_Auth, Meeting, Book
from datetime import date, timedelta, datetime
import time
from unibook.tests.helpers import LogInTester

class EditMeetingTestCase(APITestCase, LogInTester):
    """ Unit test for edit a meeting """

    fixtures = [
        'unibook/tests/fixtures/default_user.json',
        'unibook/tests/fixtures/default_club.json',
        'unibook/tests/fixtures/other_users.json',
        'unibook/tests/fixtures/other_clubs.json',
        'unibook/tests/fixtures/default_book.json',
        'unibook/tests/fixtures/other_books.json'
    ]

    def setUp(self):
        self.user = User.objects.get(username='baldunicorn')
        self.other_user = User.objects.get(username='fluffyunicorn')
        self.other_user1 = User.objects.get(username='user3')
        self.club = Club.objects.get(name='Book Club 1')
        self.other_club = Club.objects.get(name='Book Club 2')
        User_Auth.objects.create(user=self.user, rank='owner', club=self.club)
        User_Auth.objects.create(user=self.other_user, rank='member', club=self.club)
        User_Auth.objects.create(user=self.other_user1, rank='member', club=self.club)
        self.meeting = Meeting.objects.create(club=self.club,
            creator=self.other_user,
            date=(date.today() + timedelta(days=1)),
            time=time.strftime("%H:%M"),
            book=Book.objects.get(title="Clara Callan"),
            location='Bush House',
            link_to_meeting='https://examplemeeting.com',
            remote=True
        )
        self.url = reverse('edit_meeting', kwargs={'id': self.meeting.id})
        self.book = Book.objects.get(title="Classical Mythology")
        self.data = {
            'club' : self.club,
            'creator': self.other_user,
            'date': date.today() + timedelta(days=2),
            'time': time.strftime("%H:%M"),
            'book':self.book.pk,
            'location': 'Guys Bar',
            'link_to_meeting': 'https://actualmeeting.com',
            'remote': True,
        }

    def test_edit_meeting_url(self):
        """ Unit test for url validity """

        self.assertEqual(self.url, f'/unibook/edit-meeting/{self.meeting.id}/')

    def test_member_cannot_edit_another_members_meeting_if_not_owner(self):
        """ Unit test for unsuccessful edit of another members meeting """

        self.client.login(username=self.other_user1.username, password='Password123')
        self.assertTrue(self._is_logged_in())
        before_count = Meeting.objects.count()
        response = self.client.put(self.url, self.data)
        after_count = Meeting.objects.count()
        updated_meeting = Meeting.objects.get(id=self.meeting.id)
        self.assertEqual(before_count, after_count)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(updated_meeting.club, self.meeting.club)
        self.assertEqual(updated_meeting.creator, self.meeting.creator)
        self.assertEqual(updated_meeting.date, self.meeting.date)
        self.assertEqual(updated_meeting.book, self.meeting.book)
        self.assertEqual(updated_meeting.location, self.meeting.location)
        self.assertEqual(updated_meeting.link_to_meeting, self.meeting.link_to_meeting)
        self.assertEqual(updated_meeting.remote, self.meeting.remote)

    def test_cannot_change_date_to_past_date(self):
        """ Unit test for not changing past date """

        self.client.login(username=self.user.username, password='Password123')
        self.assertTrue(self._is_logged_in())
        self.data['date'] = date.today() - timedelta(days=2)
        response = self.client.put(self.url, self.data)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        meeting = Meeting.objects.get(id=self.meeting.id)
        self.assertNotEqual(meeting.date, date.today() - timedelta(days=2))
        self.assertEqual(meeting.date, self.meeting.date)

    def test_cannot_have_book_name_over_100_characters(self):
        """ Unit test for no book name over 100 character """

        self.client.login(username=self.user.username, password='Password123')
        self.assertTrue(self._is_logged_in())
        self.data['book'] = 'b'*101
        response = self.client.put(self.url, self.data)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        meeting = Meeting.objects.get(id=self.meeting.id)
        self.assertNotEqual(meeting.book, 'b'*101)
        self.assertEqual(meeting.book, self.meeting.book)

    def test_cannot_have_blank_book(self):
        self.client.login(username=self.user.username, password='Password123')
        self.assertTrue(self._is_logged_in())
        self.data['book'] = ''
        response = self.client.put(self.url, self.data)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        meeting = Meeting.objects.get(id=self.meeting.id)
        self.assertNotEqual(meeting.book, '')
        self.assertEqual(meeting.book, self.meeting.book)

    def test_cannot_have_location_over_300_characters(self):
        """ Unit test for location not over 300 characters """

        self.client.login(username=self.user.username, password='Password123')
        self.assertTrue(self._is_logged_in())
        self.data['location'] = 'l'*301
        response = self.client.put(self.url, self.data)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        meeting = Meeting.objects.get(id=self.meeting.id)
        self.assertNotEqual(meeting.location, 'l'*301)
        self.assertEqual(meeting.location, self.meeting.location)

    def test_cannot_have_blank_location(self):
        """ Unit test for no blank location """

        self.client.login(username=self.user.username, password='Password123')
        self.assertTrue(self._is_logged_in())
        self.data['location'] = ''
        response = self.client.put(self.url, self.data)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        meeting = Meeting.objects.get(id=self.meeting.id)
        self.assertNotEqual(meeting.location, '')
        self.assertEqual(meeting.location, self.meeting.location)


    def test_get_edit_meeting_when_not_logged_in(self):
        """ Test cannot edit meeting when not logged in"""

        self.assertFalse(self._is_logged_in())
        response = self.client.get(self.url, format='json')
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)
