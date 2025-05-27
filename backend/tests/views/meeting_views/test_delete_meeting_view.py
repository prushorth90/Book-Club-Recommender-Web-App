""" Unit test for delete a meeting """
from django.urls import reverse
from rest_framework.test import APITestCase
from rest_framework import status
from unibook.models import User, Club, User_Auth, Meeting, Book
from datetime import date, timedelta, datetime
import time
from unibook.tests.helpers import LogInTester

class DeleteMeetingTestCase(APITestCase, LogInTester):
    """ Unit test for delete a meeting """

    fixtures = [
        'unibook/tests/fixtures/default_user.json',
        'unibook/tests/fixtures/default_club.json',
        'unibook/tests/fixtures/other_users.json',
        'unibook/tests/fixtures/other_clubs.json',
        'unibook/tests/fixtures/default_book.json',

    ]

    def setUp(self):
        self.user = User.objects.get(username='baldunicorn')
        self.other_user = User.objects.get(username='fluffyunicorn')
        self.other_user1 = User.objects.get(username='user3')
        self.other_user2 = User.objects.get(username='user4')
        self.club = Club.objects.get(name='Book Club 1')
        User_Auth.objects.create(user=self.user, rank='owner', club=self.club)
        User_Auth.objects.create(user=self.other_user, rank='member', club=self.club)
        User_Auth.objects.create(user=self.other_user1, rank='member', club=self.club)
        User_Auth.objects.create(user=self.other_user2, rank='applicant', club=self.club)
        self.book = Book.objects.get(title="Classical Mythology")
        self.meeting = Meeting.objects.create(club=self.club,
            creator=self.other_user,
            date=(date.today() + timedelta(days=1)),
            time=time.strftime("%H:%M"),
            book=self.book,
            location='Bush House',
            link_to_meeting='https://examplemeeting.com',
            remote=True)
        self.url = reverse('delete_meeting', kwargs={'meeting_id': self.meeting.id})

    def test_delete_meeting_url(self):
        """ Unit test for delete meeting url"""

        self.assertEqual(self.url, f'/unibook/delete-meeting/{self.meeting.id}')

    def test_successful_delete_meeting_by_club_owner_who_is_not_meeting_creator(self):
        """ Unit test for successful delete meetng by club owner"""

        self.client.login(username=self.user.username, password='Password123')
        self.assertTrue(self._is_logged_in())
        count_before = Meeting.objects.count()
        response = self.client.delete(self.url)
        count_after = Meeting.objects.count()
        self.assertEqual(count_before-1, count_after)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_successful_delete_meeting_by_meeting_creator_who_is_not_club_owner(self):
        """ Unit test for successful delete meetng by meeting creator"""

        self.client.login(username=self.other_user.username, password='Password123')
        self.assertTrue(self._is_logged_in())
        count_before = Meeting.objects.count()
        response = self.client.delete(self.url)
        count_after = Meeting.objects.count()
        self.assertEqual(count_before-1, count_after)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_member_cannot_delete_another_members_meeting_if_not_owner(self):
        """ Unit test for unsuccessful delete meeting of another member """

        self.client.login(username=self.other_user1.username, password='Password123')
        self.assertTrue(self._is_logged_in())
        before_count = Meeting.objects.count()
        response = self.client.delete(self.url)
        after_count = Meeting.objects.count()
        self.assertEqual(before_count, after_count)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_applicant_cannot_delete_meeting(self):
        """ Unit test for unsuccessful delete meeting by applicant """

        self.client.login(username=self.other_user2.username, password='Password123')
        self.assertTrue(self._is_logged_in())
        before_count = Meeting.objects.count()
        response = self.client.delete(self.url)
        after_count = Meeting.objects.count()
        self.assertEqual(before_count, after_count)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_get_delete_meeting_when_not_logged_in(self):
        """ Test cannot delete meeting when not logged in"""
        
        self.assertFalse(self._is_logged_in())
        response = self.client.get(self.url, format='json')
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)
