"""Unit tests of the Message model"""
from django.core.exceptions import ValidationError, ObjectDoesNotExist
from rest_framework.test import APITestCase
from unibook.models import ChatRoom, User, Club, Message, User_Auth

class MessageModelTestCase(APITestCase):
    """Unit tests of the Message model"""

    fixtures = [
        'unibook/tests/fixtures/default_user.json',
        'unibook/tests/fixtures/other_users.json',
        'unibook/tests/fixtures/default_club.json',
        'unibook/tests/fixtures/other_clubs.json'
    ]

    def setUp(self):
        self.user = User.objects.get(username='baldunicorn')
        self.other_user = User.objects.get(username='fluffyunicorn')
        self.club = Club.objects.get(name='Book Club 1')
        User_Auth.objects.create(user=self.user, rank='owner', club=self.club)
        User_Auth.objects.create(user=self.other_user, rank='member', club=self.club)
        self.cr = ChatRoom.objects.create(
            club = self.club,
            created_by = self.user,
            name = 'room'
        )
        self.cr.members.set([self.user, self.other_user])
        self.message = Message.objects.create(
            chat_room = self.cr,
            created_by = self.user,
            message = 'Hi guys'
        )
        self.other_message = Message.objects.create(
            chat_room = self.cr,
            created_by = self.other_user,
            message = 'Nice to meet you'
        )

    def assert_message_is_valid(self):
        """Raise an error if the message is invalid."""

        try:
            self.message.full_clean()
        except (ValidationError):
            self.fail('Test message should be valid')

    def assert_message_is_invalid(self):
        """Raise an error if the message is valid."""

        with self.assertRaises(ValidationError):
            self.message.full_clean()

    def test_valid_message(self):
        """Test is the message set up is valid."""

        self.assert_message_is_valid()

    def test_chat_room_must_not_be_blank(self):
        """Test chat room must not be blank for message to be valid."""

        self.message.chat_room = None
        self.assert_message_is_invalid()

    def test_all_messages_in_chat_room_deleted_if_chat_room_deleted(self):
        """Test messages are deleted in the chat room is deleted."""

        before_count = Message.objects.filter(chat_room=self.cr).count()
        self.cr.delete()
        after_count = Message.objects.filter(chat_room=self.cr).count()
        self.assertNotEqual(before_count, 0)
        self.assertEqual(after_count, 0)

    def test_created_by_must_not_be_blank(self):
        """Test created by must not be blank for message to be valid."""

        self.message.created_by = None
        self.assert_message_is_invalid()

    def test_all_messages_from_user_deleted_if_user_deleted(self):
        """Test all the messages are deleted if the user that sent the messages are deleted."""

        before_count = Message.objects.filter(chat_room=self.cr).count()
        self.other_user.delete()
        after_count = Message.objects.filter(chat_room=self.cr).count()
        self.assertNotEqual(before_count, after_count)
        self.assertNotEqual(after_count, 0)

    def test_message_must_not_be_blank(self):
        """Test message must not be blank for message to be valid."""

        self.message.message = None
        self.assert_message_is_invalid()
