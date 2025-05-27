"""Unit tests for meeting serializer."""
from datetime import date, timedelta
from unibook.models import Meeting, Club,User, Book, User_Auth
from unibook.serializers import MeetingSerializer
from rest_framework.test import APITestCase

class MeetingSerializerTestCase(APITestCase):
    """Unit tests for meeting serializer."""
    fixtures = [
        'unibook/tests/fixtures/default_user.json',
        'unibook/tests/fixtures/default_club.json',
        'unibook/tests/fixtures/default_book.json'
    ]

    def setUp(self):
        self.club = Club.objects.get(name='Book Club 1')
        self.owner = User.objects.get(username='baldunicorn')
        self.book = Book.objects.get(isbn='0195153448')
        User_Auth.objects.create(user=self.owner, club=self.club, rank='owner')

        self.serializer_data = {
            'club': self.club.pk,
            'creator': self.owner,
            'date': date.today()+timedelta(days=3),
            'time':'09:00',
            'book':self.book.isbn,
            'location': 'Bush House',

        }

    def test_valid_meeting_serializer(self):
        """Test the serializer to create a valid meeting."""

        serializer = MeetingSerializer(data=self.serializer_data)
        self.assertTrue(serializer.is_valid())

    def test_serializer_has_necessary_fields(self):
        """Test the serializer to check if it has necessary fields."""

        serializer = MeetingSerializer()
        self.assertIn('club', serializer.fields)
        self.assertIn('creator', serializer.fields)
        self.assertIn('date', serializer.fields)
        self.assertIn('time', serializer.fields)
        self.assertIn('book', serializer.fields)
        self.assertIn('location', serializer.fields)

    def test_serializer_saves_correctly(self):
        """Test that the serializer saves correctly."""

        serializer = MeetingSerializer(data=self.serializer_data)
        before_count = Meeting.objects.count()
        serializer.is_valid()
        serializer.save()
        after_count = Meeting.objects.count()
        self.assertEqual(after_count, before_count + 1)
        meeting = Meeting.objects.get(id=1)
        self.assertEqual(meeting.club.name, 'Book Club 1')
        self.assertEqual(meeting.creator.username, 'baldunicorn')
        self.assertEqual(meeting.book.title, 'Classical Mythology')
        self.assertEqual(meeting.location, 'Bush House')

    def test_club_must_not_be_blank(self):
        """Test for the invalid serializer that can't be saved when club blank."""

        self.serializer_data['club'] = None
        serializer = MeetingSerializer(data=self.serializer_data)
        before_count = Meeting.objects.count()
        with self.assertRaises(AssertionError):
            serializer.save()
        after_count = Meeting.objects.count()
        self.assertEqual(after_count, before_count)

    def test_book_must_not_be_blank(self):
        """Test for the invalid serializer that can't be saved when book blank."""

        self.serializer_data['book'] = None
        serializer = MeetingSerializer(data=self.serializer_data)
        before_count = Meeting.objects.count()
        with self.assertRaises(AssertionError):
            serializer.save()
        after_count = Meeting.objects.count()
        self.assertEqual(after_count, before_count)

    def test_creator_must_not_be_blank(self):
        """Test for the invalid serializer that can't be saved when creator blank."""

        self.serializer_data['creator'] = None
        serializer = MeetingSerializer(data=self.serializer_data)
        before_count = Meeting.objects.count()
        with self.assertRaises(AssertionError):
            serializer.save()
        after_count = Meeting.objects.count()
        self.assertEqual(after_count, before_count)

    def test_date_must_not_be_blank(self):
        """Test for the invalid serializer that can't be saved when date blank."""

        self.serializer_data['date'] = ''
        serializer = MeetingSerializer(data=self.serializer_data)
        before_count = Meeting.objects.count()
        with self.assertRaises(AssertionError):
            serializer.save()
        after_count = Meeting.objects.count()
        self.assertEqual(after_count, before_count)

    def test_time_must_not_be_blank(self):
        """Test for the invalid serializer that can't be saved when time blank."""

        self.serializer_data['time'] = ''
        serializer = MeetingSerializer(data=self.serializer_data)
        before_count = Meeting.objects.count()
        with self.assertRaises(AssertionError):
            serializer.save()
        after_count = Meeting.objects.count()
        self.assertEqual(after_count, before_count)

    def test_date_not_past_date(self):
        """Test for the invalid serializer that can't be saved when use past date"""

        self.serializer_data['date'] = date.today() - timedelta(days=1)
        serializer = MeetingSerializer(data=self.serializer_data)
        before_count = Meeting.objects.count()
        with self.assertRaises(AssertionError):
            serializer.save()
        after_count = Meeting.objects.count()
        self.assertEqual(after_count, before_count)

    def test_time_must_use_correct_hour_format(self):
        """Test for the invalid serializer that can't be saved when time hour format."""

        self.serializer_data['time'] = '100:20'
        serializer = MeetingSerializer(data=self.serializer_data)
        before_count = Meeting.objects.count()
        with self.assertRaises(AssertionError):
            serializer.save()
        after_count = Meeting.objects.count()
        self.assertEqual(after_count, before_count)

    def test_time_must_use_correct_minute_format(self):
        """Test for the invalid serializer that can't be saved when time min format"""

        self.serializer_data['time'] = '10:200'
        serializer = MeetingSerializer(data=self.serializer_data)
        before_count = Meeting.objects.count()
        with self.assertRaises(AssertionError):
            serializer.save()
        after_count = Meeting.objects.count()
        self.assertEqual(after_count, before_count)

    def test_link_to_meeting_must_have_scheme(self):
        """Test for the invalid serializer that can't be saved when time blank."""

        self.serializer_data['link_to_meeting'] = 'teams.microsoft.com/l/meetup-join/19%3ameeting_OGRkYTEwOGUtODcwMS00NjhjLTk2MmQtMmNkYTg2ZTU0MTc2%40thread.v2/0?context=%7b%22Tid%22%3a%228370cf14-16f3-4c16-b83c-724071654356%22%2c%22Oid%22%3a%221980b7c3-6193-437c-8e58-3860d9a4a39c%22%7d'
        serializer = MeetingSerializer(data=self.serializer_data)
        before_count = Meeting.objects.count()
        with self.assertRaises(AssertionError):
            serializer.save()
        after_count = Meeting.objects.count()
        self.assertEqual(after_count, before_count)
