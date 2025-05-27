"""Unit tests for Club model."""
from unibook.models import Club
from django.core.exceptions import ValidationError
from rest_framework.test import APITestCase

class ClubModelTestCase(APITestCase):
    """Unit tests for Club model."""

    fixtures = [
        'unibook/tests/fixtures/default_club.json',
        'unibook/tests/fixtures/other_clubs.json',
    ]

    def setUp(self):
        self.club = Club.objects.get(name='Book Club 1')
        self.second_club = Club.objects.get(name='Book Club 2')

    def assert_club_is_valid(self):
        """Raise an error if club is invalid."""

        try:
            self.club.full_clean()
        except (ValidationError):
            self.fail('Test club needs to be made valid')

    def assert_club_is_invalid(self):
        """Raise an error if club is valid."""

        with self.assertRaises(ValidationError):
            self.club.full_clean()

    def test_valid_club(self):
        """Check if the club is valid."""

        self.assert_club_is_valid()

    """ Unit test for name """

    def test_name_must_be_unique(self):
        self.club.name = self.second_club.name
        self.assert_club_is_invalid()

    def test_name_must_not_be_longer_than_50_characters(self):
        self.club.name = 'o' * 51
        self.assert_club_is_invalid()

    def test_name_can_have_50_characters(self):
        self.club.name = 'o' * 50
        self.assert_club_is_valid()

    def test_name_can_have_numbers(self):
        self.club.name = '1'
        self.assert_club_is_valid()

    def test_name_can_have_letters_and_numbers(self):
        self.club.name = '2a'
        self.assert_club_is_valid()

    def test_name_must_not_be_blank(self):
        self.club.name = ''
        self.assert_club_is_invalid()

    """ Unit test for description """

    def test_description_need_not_be_unique(self):
        self.club.description = self.second_club.description
        self.assert_club_is_valid()

    def test_description_must_not_be_longer_500_characters(self):
        self.club.description = 'o' * 501
        self.assert_club_is_invalid()

    def test_description_can_have_numbers(self):
        self.club.description = '32'
        self.assert_club_is_valid()

    def test_description_can_have_500_characters(self):
        self.club.description = 'o' * 500
        self.assert_club_is_valid()

    def test_description_can_have_letters_and_numbers(self):
        self.club.name = '2a'
        self.assert_club_is_valid()

    def test_description_cannot_be_blank(self):
        self.club.description = ''
        self.assert_club_is_invalid()

    """ Unit test for description """

    def test_members_capacity_need_not_be_unique(self):
        self.club.members_capacity = self.second_club.members_capacity
        self.assert_club_is_valid()

    def test_members_capacity_cannot_be_greater_than_50(self):
        self.club.members_capacity = 51
        self.assert_club_is_invalid()

    def test_members_capacity_cannot_be_lesser_than_2(self):
        self.club.members_capacity = 1
        self.assert_club_is_invalid()

    def test_members_capacity_cannot_be_negative(self):
        self.club.members_capacity = -1
        self.assert_club_is_invalid()

    def test_members_capacity_can_be_50(self):
        self.club.members_capacity = 50
        self.assert_club_is_valid()

    def test_members_capacity_can_be_2(self):
        self.club.members_capacity = 2
        self.assert_club_is_valid()

    def test_members_capacity_cannot_be_letters(self):
        self.club.members_capacity = 'a'
        self.assert_club_is_invalid()
