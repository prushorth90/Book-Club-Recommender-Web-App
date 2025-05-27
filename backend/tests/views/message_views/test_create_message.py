"""Unit tests for create message view."""
from django.urls import reverse
from unibook.models import Message, ChatRoom, User, Club, User_Auth
from unibook.tests.helpers import LogInTester
from rest_framework import status
from rest_framework.test import APITestCase

class CreateMessageTests(APITestCase, LogInTester):
    """Unit tests for create message view."""

    fixtures = ['unibook/tests/fixtures/default_user.json',
                'unibook/tests/fixtures/other_users.json',
                'unibook/tests/fixtures/default_club.json',
                'unibook/tests/fixtures/other_clubs.json']

    def setUp(self):
        self.user = User.objects.get(username='baldunicorn')
        self.club = Club.objects.get(name='Book Club 1')
        self.other_user = User.objects.get(username = 'fluffyunicorn')
        self.other_club = Club.objects.get(name = 'Book Club 2')
        User_Auth.objects.create(user=self.user, rank='owner', club=self.club)
        User_Auth.objects.create(user=self.other_user, rank='owner', club=self.other_club)
        self.chat_room = ChatRoom.objects.create(club=self.club, name='tester', created_by=self.user)
        self.url = (f'/unibook/messages/')
        self.data={
            'chat_room': self.chat_room.pk,
            'message': 'hi there',
            'created_by': self.user.pk
        }
        self.other_data={
            'chat_room': self.chat_room.pk,
            'message': 'hi there',
            'created_by': self.other_user.pk
        }

    def test_user_in_chat_room_can_post_message(self):
        """Test for user in a chat room successfully post a message."""

        self.client.login(username=self.user.username, password='Password123')
        self.assertTrue(self._is_logged_in())
        count_before = Message.objects.count()
        response = self.client.post(self.url, self.data)
        count_after = Message.objects.count()
        self.assertEqual(count_after, count_before+1)
