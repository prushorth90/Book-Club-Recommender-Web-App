"""Unit tests for User_Auth model."""
from unibook.models import Club, User_Auth, User
from django.core.exceptions import ValidationError, ObjectDoesNotExist
from rest_framework.test import APITestCase

class UserAuthModelTest(APITestCase):
    """Unit tests for User_Auth model."""

    fixtures = [
        'unibook/tests/fixtures/default_user.json',
        'unibook/tests/fixtures/default_club.json'
    ]

    def setUp(self):
        self.user = User.objects.get(username='baldunicorn')
        self.club = Club.objects.get(name='Book Club 1')
        self.user_auth = User_Auth.objects.create(
            user=self.user,
            club=self.club,
            rank='owner'
        )

    def assert_user_auth_is_valid(self):
        """Raise an error if user auth is invalid."""

        try:
            self.user_auth.full_clean()
        except (ValidationError):
            self.fail('Test user auth needs to be made valid')

    def assert_user_auth_is_invalid(self):
        """Raise an error if user auth is valid."""

        with self.assertRaises(ValidationError):
            self.user_auth.full_clean()

    def test_valid_user_auth(self):
        """Test if the user auth set up is valid."""

        self.assert_user_auth_is_valid()

    """ Unit test for user """

    def test_user_must_not_be_blank(self):
        self.user_auth.user = None
        self.assert_user_auth_is_invalid()

    def test_user_auth_is_deleted_if_user_is_deleted(self):
        self.user.delete()
        with self.assertRaises(ObjectDoesNotExist):
            User_Auth.objects.get(id=self.user_auth.id)

    """Unit tests for authorization"""

    def test_authorization_must_be_valid_choice(self):
        self.user_auth.rank = "aaa"
        self.assert_user_auth_is_invalid()

    def test_authorization_must_not_be_blank(self):
        self.user_auth.rank = ""
        self.assert_user_auth_is_invalid()

    """ Unit test for club"""

    def test_club_must_not_be_blank(self):
        self.user_auth.club = None
        self.assert_user_auth_is_invalid()

    def test_user_auth_is_deleted_if_club_is_deleted(self):
        self.club.delete()
        with self.assertRaises(ObjectDoesNotExist):
            User_Auth.objects.get(id=self.user_auth.id)
