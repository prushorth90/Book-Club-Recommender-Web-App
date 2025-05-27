"""Unit tests for Meeting model."""
from unibook.models import Club, Meeting, Book, User
from django.core.exceptions import ValidationError, ObjectDoesNotExist
from django.db import IntegrityError
from datetime import date, timedelta
from rest_framework.test import APITestCase

class MeetingModelTestCase(APITestCase):
    """Unit tests for Meeting model."""

    fixtures = [
        'unibook/tests/fixtures/default_user.json',
        'unibook/tests/fixtures/default_club.json',
        'unibook/tests/fixtures/default_book.json',
    ]

    def setUp(self):
        self.creator = User.objects.get(username='baldunicorn')
        self.club = Club.objects.get(name='Book Club 1')
        self.book = Book.objects.get(isbn='0195153448')
        self.meeting = Meeting.objects.create(
            club=self.club,
            creator=self.creator,
            date=date.today(),
            time='09:00',
            book=self.book,
            location='Bush House'
        )
        self.second_meeting = Meeting.objects.create(
            club=self.club,
            creator=self.creator,
            date=date.today() + timedelta(days=3),
            time='12:00',
            book=self.book,
            location='remote',
            link_to_meeting='https://teams.microsoft.com/l/meetup-join/19%3ameeting_OGRkYTEwOGUtODcwMS00NjhjLTk2MmQtMmNkYTg2ZTU0MTc2%40thread.v2/0?context=%7b%22Tid%22%3a%228370cf14-16f3-4c16-b83c-724071654356%22%2c%22Oid%22%3a%221980b7c3-6193-437c-8e58-3860d9a4a39c%22%7d',
            remote=True
        )

    def assert_meeting_is_valid(self):
        """Raise an error if the meeting is invalid."""

        try:
            self.meeting.full_clean()
        except (ValidationError):
            self.fail('Test meeting needs to be made valid')

    def assert_meeting_is_invalid(self):
        """Raise an error if the meeting is valid."""

        with self.assertRaises(ValidationError):
            self.meeting.full_clean()

    def test_valid_meeting(self):
        """Tests if the meeting set up is valid."""

        self.assert_meeting_is_valid()

    def test_meeting_club_date_time_must_be_unique(self):
        """Test meeting must be unique with club, date and time."""

        with self.assertRaises(IntegrityError):
            Meeting.objects.create(
                club=self.meeting.club,
                date=self.meeting.date,
                time=self.meeting.time,
                book=self.meeting.book,
                location='remote'
            )

    """ Unit test for club """

    def test_club_must_not_be_blank(self):
        self.meeting.club = None
        self.assert_meeting_is_invalid()

    def test_meeting_is_deleted_if_club_is_deleted(self):
        self.club.delete()
        with self.assertRaises(ObjectDoesNotExist):
            Meeting.objects.get(id=self.meeting.id)

    """ Unit test for creator """

    def test_creator_must_not_be_blank(self):
        self.meeting.creator = None
        self.assert_meeting_is_invalid()

    def test_meeting_is_deleted_if_creator_is_deleted(self):
        self.creator.delete()
        with self.assertRaises(ObjectDoesNotExist):
            Meeting.objects.get(id=self.meeting.id)

    """ Unit test for book """

    def test_book_must_not_be_blank(self):
        self.meeting.book = None
        self.assert_meeting_is_invalid()

    def test_meeting_book_is_none_if_book_is_deleted(self):
        self.book.delete()
        self.meeting = Meeting.objects.get(id=self.meeting.id)
        self.assertEqual(self.meeting.book, None)

    """ Unit test for date """

    def test_date_must_not_be_past_date(self):
        self.meeting.date = date.today() - timedelta(days=1)
        self.assert_meeting_is_invalid()

    def test_date_can_have_future_date(self):
        self.meeting.date = date.today() + timedelta(days=1)
        self.assert_meeting_is_valid()

    def test_date_must_not_be_blank(self):
        self.meeting.date = ''
        self.assert_meeting_is_invalid()

    def test_meeting_can_have_same_date_as_other_meeting(self):
        self.meeting.date = self.second_meeting.date
        self.assert_meeting_is_valid()

    """ Unit tests for time """

    def test_time_must_use_correct_hour_format(self):
        self.meeting.time = "100:30"
        self.assert_meeting_is_invalid()

    def test_time_must_use_correct_minute_format(self):
        self.meeting.time = "10:100"
        self.assert_meeting_is_invalid()

    def test_time_must_not_be_blank(self):
        self.meeting.time = ''
        self.assert_meeting_is_invalid()

    def test_meeting_can_have_same_time_as_other_meeting(self):
        self.meeting.time = self.second_meeting.time
        self.assert_meeting_is_valid()

    """ Unit tests for location """

    def test_location_must_not_be_blank(self):
        self.meeting.location = ''
        self.assert_meeting_is_invalid()

    def test_location_need_not_be_unique(self):
        self.meeting.location = self.second_meeting.location
        self.assert_meeting_is_valid()

    def test_location_can_have_300_characters(self):
        self.meeting.location = 'l' * 300
        self.assert_meeting_is_valid()

    def test_location_must_not_be_greater_than_300_characters(self):
        self.meeting.location = 'l' * 301
        self.assert_meeting_is_invalid()

    """Unit tests for link to meeting """

    def test_link_to_meeting_can_be_blank(self):
        self.meeting.link_to_meeting = ''
        self.assert_meeting_is_valid()

    def test_link_to_meeting_need_not_be_unique(self):
        self.meeting.link_to_meeting = self.second_meeting.link_to_meeting
        self.assert_meeting_is_valid()

    def test_link_to_meeting_must_have_scheme(self):
        self.meeting.link_to_meeting = 'teams.microsoft.com/l/meetup-join/19%3ameeting_OGRkYTEwOGUtODcwMS00NjhjLTk2MmQtMmNkYTg2ZTU0MTc2%40thread.v2/0?context=%7b%22Tid%22%3a%228370cf14-16f3-4c16-b83c-724071654356%22%2c%22Oid%22%3a%221980b7c3-6193-437c-8e58-3860d9a4a39c%22%7d'
        self.assert_meeting_is_invalid()

    def test_link_to_meeting_must_have_domain_name(self):
        self.meeting.link_to_meeting = 'https://l/meetup-join/19%3ameeting_OGRkYTEwOGUtODcwMS00NjhjLTk2MmQtMmNkYTg2ZTU0MTc2%40thread.v2/0?context=%7b%22Tid%22%3a%228370cf14-16f3-4c16-b83c-724071654356%22%2c%22Oid%22%3a%221980b7c3-6193-437c-8e58-3860d9a4a39c%22%7d'
        self.assert_meeting_is_invalid()

    def test_link_to_meeting_must_not_have_two_consecutive_dots(self):
        self.meeting.link_to_meeting = 'https://teams.microsoft..com/l/meetup-join/19%3ameeting_OGRkYTEwOGUtODcwMS00NjhjLTk2MmQtMmNkYTg2ZTU0MTc2%40thread.v2/0?context=%7b%22Tid%22%3a%228370cf14-16f3-4c16-b83c-724071654356%22%2c%22Oid%22%3a%221980b7c3-6193-437c-8e58-3860d9a4a39c%22%7d'
        self.assert_meeting_is_invalid()

    def test_link_to_meeting_must_not_have_dot_before_domain_name(self):
        self.meeting.link_to_meeting = 'https://.teams.microsoft.com/l/meetup-join/19%3ameeting_OGRkYTEwOGUtODcwMS00NjhjLTk2MmQtMmNkYTg2ZTU0MTc2%40thread.v2/0?context=%7b%22Tid%22%3a%228370cf14-16f3-4c16-b83c-724071654356%22%2c%22Oid%22%3a%221980b7c3-6193-437c-8e58-3860d9a4a39c%22%7d'
        self.assert_meeting_is_invalid()

    """Unit tests for link to meeting """

    def test_remote_must_not_be_blank(self):
        self.meeting.remote = ''
        self.assert_meeting_is_invalid()

    def test_remote_need_not_be_unique(self):
        self.meeting.remote = self.second_meeting.remote
        self.assert_meeting_is_valid()

    def test_remote_must_be_boolean(self):
        self.meeting.remote = 'a'
        self.assert_meeting_is_invalid()
