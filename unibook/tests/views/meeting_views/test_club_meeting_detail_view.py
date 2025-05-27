"""Unit tests for the club meeting detail view."""
from datetime import date, timedelta
from django.urls import reverse
from rest_framework.test import APITestCase
from rest_framework import status
from unibook.models import User,User_Auth,Club,Meeting,Book
from unibook.tests.helpers import LogInTester

class ClubMeetingDetailViewTestCase(APITestCase, LogInTester):
    """Unit tests for the club meeting detail view."""

    fixtures = [
        'unibook/tests/fixtures/default_user.json',
        'unibook/tests/fixtures/other_users.json',
        'unibook/tests/fixtures/default_club.json',
        'unibook/tests/fixtures/default_book.json'
    ]

    def setUp(self):
        self.owner = User.objects.get(username='baldunicorn')
        self.member = User.objects.get(username='fluffyunicorn')
        self.applicant = User.objects.get(username='user3')
        self.wrong_user = User.objects.get(username='user4')
        self.club = Club.objects.get(name='Book Club 1')

        User_Auth.objects.create(user=self.owner, club=self.club, rank='owner')
        User_Auth.objects.create(user=self.member, club=self.club, rank='member')
        User_Auth.objects.create(user=self.applicant, club=self.club, rank='applicant')

        self.book = Book.objects.get(isbn='0195153448')
        self.meeting = Meeting.objects.create(
            club=self.club,
            creator=self.owner,
            date=date.today()+timedelta(days=3),
            time='09:00',
            book=self.book,
            location='Bush House'
        )

        self.url = reverse('meeting_detail', kwargs={'club_id': self.club.id})

    def test_club_meeting_detail_url(self):
        """Unit test for club meeting detail url."""

        self.assertEqual(self.url, f'/unibook/meeting-detail/{self.meeting.id}/')

    def test_get_club_meeting_detail_when_not_logged_in(self):
        """Test for user not being able to view the meeting detail when not logged in."""

        self.assertFalse(self._is_logged_in())
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_get_club_meeting_detail_by_owner(self):
        """Test for owner successfully viewing a meeting in the club."""

        self.client.login(username=self.owner.username, password='Password123')
        self.assertTrue(self._is_logged_in())
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_get_club_meeting_detail_by_member(self):
        """Test for member successfully viewing a meeting in the club."""

        self.client.login(username=self.owner.username, password='Password123')
        self.assertTrue(self._is_logged_in())
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
