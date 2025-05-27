"""Unit tests of the Chat Room model"""
from django.core.exceptions import ValidationError, ObjectDoesNotExist
from rest_framework.test import APITestCase
from unibook.models import ChatRoom, User, Club

class ChatRoomModelTestCase(APITestCase):
    """Unit tests of the Chat Room model"""

    fixtures = [
        'unibook/tests/fixtures/default_user.json',
        'unibook/tests/fixtures/other_users.json',
        'unibook/tests/fixtures/default_club.json',
        'unibook/tests/fixtures/other_clubs.json'
    ]

    def setUp(self):
        self.creator = User.objects.get(username='baldunicorn')
        self.user2 = User.objects.get(username='fluffyunicorn')
        self.members = [self.creator, self.user2]
        self.club = Club.objects.get(name='Book Club 1')
        self.chat_room = ChatRoom.objects.create(
            club = self.club,
            created_by = self.creator,
            name='chat room 1'
        )
        self.chat_room.members.set(self.members)

        self.other_creator = User.objects.get(username='user3')
        self.other_user2 = User.objects.get(username='user4')
        self.other_members = [self.creator, self.user2]
        self.second_club = Club.objects.get(name='Book Club 2')
        self.second_chat_room = ChatRoom.objects.create(
            club = self.second_club,
            created_by = self.other_creator,
            name='chat room 2'
        )
        self.second_chat_room.members.set(self.other_members)

    def assert_chat_room_is_valid(self):
        """Raise an error if the chat room is invalid."""

        try:
            self.chat_room.full_clean()
        except (ValidationError):
            self.fail('Test chat room should be valid')

    def assert_chat_room_is_invalid(self):
        """Raise an error if the chat room is valid."""

        with self.assertRaises(ValidationError):
            self.chat_room.full_clean()

    def test_valid_chat_room(self):
        """Test is the chat room set up is valid."""

        self.assert_chat_room_is_valid()

    """ Unit test for created_by """

    def test_created_by_must_not_be_blank(self):
        self.chat_room.created_by = None
        self.assert_chat_room_is_invalid()

    def test_chat_room_is_deleted_if_created_by_is_deleted(self):
        self.creator.delete()
        with self.assertRaises(ObjectDoesNotExist):
            ChatRoom.objects.get(id=self.chat_room.id)

    """ Unit test for name """

    def test_name_need_not_be_unique(self):
        self.chat_room.name = self.second_chat_room.name
        self.assert_chat_room_is_valid()

    def test_name_must_not_be_blank(self):
        self.chat_room.name = ''
        self.assert_chat_room_is_invalid()

    def test_name_must_not_be_greater_than_255_characters(self):
        self.chat_room.name = 'x' * 256
        self.assert_chat_room_is_invalid()

    def test_name_can_be_255_characters(self):
        self.chat_room.name = 'x' * 255
        self.assert_chat_room_is_valid()

    """ Unit test for timestamp """

    def test_timestamp_need_not_be_unique(self):
        self.chat_room.timestamp = self.second_chat_room.timestamp
        self.assert_chat_room_is_valid()

    """ Unit test for club """

    def test_club_must_not_be_blank(self):
        self.chat_room.club = None
        self.assert_chat_room_is_invalid()

    def test_chat_room_is_deleted_if_club_is_deleted(self):
        self.club.delete()
        with self.assertRaises(ObjectDoesNotExist):
            ChatRoom.objects.get(id=self.chat_room.id)
