"""Unit tests of the ChangePassword Serializer"""
from unibook.models import User
from unibook.serializers import ChangePasswordSerializer
from rest_framework.test import APITestCase

class ChangePasswordSerializerTestCase(APITestCase):
    """Unit tests of the ChangePassword Serializer"""

    fixtures = ['unibook/tests/fixtures/default_user.json']

    def setUp(self):
        self.user = User.objects.get(username='baldunicorn')
        self.serializer_data = {
            'old_password': 'Password123',
            'new_password': 'NewPassword123',
        }

    def test_serializer_has_necessary_fields(self):
        """Test serializer has necessary fields."""

        serializer = ChangePasswordSerializer()
        self.assertIn('old_password', serializer.fields)
        self.assertIn('new_password', serializer.fields)

    def test_valid_change_password_serializer(self):
        """Test serializer is valid if given correct data."""

        serializer = ChangePasswordSerializer(data=self.serializer_data)
        self.assertTrue(serializer.is_valid())

    def test_new_password_must_contain_uppercase_character(self):
        """Test that the new password must contain an uppercase character to be made valid."""

        self.serializer_data['new_password'] = 'password123'
        serializer = ChangePasswordSerializer(data=self.serializer_data)
        self.assertFalse(serializer.is_valid())

    def test_new_password_must_contain_lowercase_character(self):
        """Test that the new password must contain an lowercase character to be made valid."""

        self.serializer_data['new_password'] = 'PASSWORD123'
        serializer = ChangePasswordSerializer(data=self.serializer_data)
        self.assertFalse(serializer.is_valid())

    def test_new_password_must_contain_number(self):
        """Test that the new password must contain a number to be made valid."""

        self.serializer_data['new_password'] = 'PasswordABC'
        serializer = ChangePasswordSerializer(data=self.serializer_data)
        self.assertFalse(serializer.is_valid())
