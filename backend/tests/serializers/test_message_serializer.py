"""Unit tests for message serializer."""
from unibook.models import Club, User, Message, ChatRoom
from unibook.serializers import MessageSerializer
from rest_framework.test import APITestCase

class MessageSerializerTestCase(APITestCase):
    """Unit tests for message serializer."""

    fixtures = [
        'unibook/tests/fixtures/default_user.json',
        'unibook/tests/fixtures/default_club.json'
    ]

    def setUp(self):
        self.user = User.objects.get(username='baldunicorn')
        self.club = Club.objects.get(name='Book Club 1')
        self.cr = ChatRoom.objects.create(
            club = self.club,
            created_by = self.user,
            name = 'room'
        )
        self.cr.members.set([self.user])
        self.serializer_data = {
            'chat_room': self.cr.pk,
            'message': 'Hello amigos',
            'created_by': self.user.pk
        }

    def test_valid_message_serializer(self):
        """Test the serializer to create a valid message"""

        serializer = MessageSerializer(data=self.serializer_data)
        self.assertTrue(serializer.is_valid())

    def test_serializer_has_necessary_fields(self):
        """Test the serializer to check if it has necessary fields."""

        serializer = MessageSerializer()
        self.assertIn('chat_room', serializer.fields)
        self.assertIn('message', serializer.fields)
        self.assertIn('timestamp', serializer.fields)
        self.assertIn('created_by', serializer.fields)

    def test_serializer_saves_correctly(self):
        """Test that the serializer saves correctly."""

        serializer = MessageSerializer(data=self.serializer_data)
        before_count = Message.objects.count()
        serializer.is_valid()
        serializer.save()
        after_count = Message.objects.count()
        self.assertEqual(before_count+1, after_count)
        message = Message.objects.get(id=1)
        self.assertEqual(message.chat_room, self.cr)
        self.assertEqual(message.message, 'Hello amigos')
        self.assertEqual(message.created_by, self.user)

    def test_chat_room_must_not_be_blank(self):
        """Test that the chat room must be not blank."""

        self.serializer_data['chat_room'] = ''
        serializer = MessageSerializer(data=self.serializer_data)
        before_count = Message.objects.count()
        with self.assertRaises(AssertionError):
            serializer.save()
        after_count = Message.objects.count()
        self.assertEqual(after_count, before_count)

    def test_message_must_not_be_blank(self):
        """Test that the message must be not blank."""

        self.serializer_data['message'] = ''
        serializer = MessageSerializer(data=self.serializer_data)
        before_count = Message.objects.count()
        with self.assertRaises(AssertionError):
            serializer.save()
        after_count = Message.objects.count()
        self.assertEqual(after_count, before_count)

    def test_created_by_must_not_be_blank(self):
        """Test that the created by must be not blank."""

        self.serializer_data['created_by'] = ''
        serializer = MessageSerializer(data=self.serializer_data)
        before_count = Message.objects.count()
        with self.assertRaises(AssertionError):
            serializer.save()
        after_count = Message.objects.count()
        self.assertEqual(after_count, before_count)
