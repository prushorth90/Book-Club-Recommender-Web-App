""" Unit tests for sign up serializer """
from django.contrib.auth.hashers import check_password
from unibook.models import User
from unibook.serializers import SignUpSerializer
from rest_framework.test import APITestCase

class SignUpSerializerTestCase(APITestCase):
    """Unit tests for sign up serializer."""

    def setUp(self):
        self.serializer_data = {
          'username': 'baldunicorn',
          'first_name': 'Bald',
          'last_name': 'Unicorn',
          'email': 'baldunicorn@example.org',
          'bio': 'Books are the best!',
          'password': 'Password123',
        }

    def test_password_cannot_be_blank(self):
        """Test for the invalid serializer that can be saved when the password is blank."""

        self.serializer_data['password'] = ''
        serializer = SignUpSerializer(data=self.serializer_data)
        self.assertFalse(serializer.is_valid())
        before_count = User.objects.count()
        with self.assertRaises(AssertionError):
            serializer.save()
        after_count = User.objects.count()
        self.assertEqual(after_count, before_count)

    def test_valid_sign_up_serializer(self):
        """Test the serializer to create a valid user."""

        serializer = SignUpSerializer(data=self.serializer_data)
        self.assertTrue(serializer.is_valid())

    def test_serializer_has_necessary_fields(self):
        """Test the serializer to check if it has necessary fields."""

        serializer = SignUpSerializer()
        self.assertIn('username', serializer.fields)
        self.assertIn('first_name', serializer.fields)
        self.assertIn('last_name', serializer.fields)
        self.assertIn('email', serializer.fields)
        self.assertIn('bio', serializer.fields)
        self.assertIn('password', serializer.fields)


    def test_serializer_saves_correctly(self):
        """Test that the serializer saves correctly."""

        serializer = SignUpSerializer(data=self.serializer_data)
        before_count = User.objects.count()
        serializer.is_valid()
        serializer.save()
        after_count = User.objects.count()
        self.assertEqual(after_count, before_count + 1)
        user = User.objects.get(username="baldunicorn")
        self.assertEqual(user.username, 'baldunicorn')
        self.assertEqual(user.first_name, 'Bald')
        self.assertEqual(user.last_name, 'Unicorn')
        self.assertEqual(user.email, 'baldunicorn@example.org')
        self.assertEqual(user.bio, 'Books are the best!')
        check_password(user.password, 'Password123')


    def test_username_must_not_be_longer_50_characters(self):
        """Test for the invalid serializer that can't be saved when the username contains more than 50 characters."""

        self.serializer_data['username'] = 'b' * 51
        serializer = SignUpSerializer(data=self.serializer_data)
        self.assertFalse(serializer.is_valid())
        before_count = User.objects.count()
        with self.assertRaises(AssertionError):
            serializer.save()
        after_count = User.objects.count()
        self.assertEqual(after_count, before_count)

    def test_username_can_be_50_characters_(self):
        """Test for the invalid serializer that can be saved when the username contains 50 characterss."""

        self.serializer_data['username'] = 'b' * 50
        serializer = SignUpSerializer(data=self.serializer_data)
        self.assertTrue(serializer.is_valid())
        before_count = User.objects.count()
        serializer.save()
        after_count = User.objects.count()
        self.assertEqual(after_count, before_count+1)

    def test_username_can_be_3_characters(self):
        """Test for the invalid serializer that can be saved when the username contains 50 characters."""

        self.serializer_data['username'] = 'b' * 3
        serializer = SignUpSerializer(data=self.serializer_data)
        self.assertTrue(serializer.is_valid())
        before_count = User.objects.count()
        serializer.save()
        after_count = User.objects.count()
        self.assertEqual(after_count, before_count+1)

    def test_username_can_between_3_and_50_characters(self):
        """Test for the invalid serializer that can be saved when the username between 3 and 50 characters."""

        self.serializer_data['username'] = 'b' * 9
        serializer = SignUpSerializer(data=self.serializer_data)
        self.assertTrue(serializer.is_valid())
        before_count = User.objects.count()
        serializer.save()
        after_count = User.objects.count()
        self.assertEqual(after_count, before_count+1)

    def test_username_cannot_be_2_characters(self):
        """Test for the invalid serializer that cannot be saved when the username contains 2 characterss."""

        self.serializer_data['username'] = 'b' * 2
        serializer = SignUpSerializer(data=self.serializer_data)
        self.assertFalse(serializer.is_valid())
        before_count = User.objects.count()
        with self.assertRaises(AssertionError):
            serializer.save()
        after_count = User.objects.count()
        self.assertEqual(after_count, before_count)

    def test_username_must_not_be_blank(self):
        """Test for the invalid serializer that can't be saved when the username is blank."""

        self.serializer_data['username'] = ''
        serializer = SignUpSerializer(data=self.serializer_data)
        self.assertFalse(serializer.is_valid())
        before_count = User.objects.count()
        with self.assertRaises(AssertionError):
            serializer.save()
        after_count = User.objects.count()
        self.assertEqual(after_count, before_count)

    def test_email_must_not_be_blank(self):
        """Test for the invalid serializer that can't be saved when the email is blank."""

        self.serializer_data['email'] = ''
        serializer = SignUpSerializer(data=self.serializer_data)
        self.assertFalse(serializer.is_valid())
        before_count = User.objects.count()
        with self.assertRaises(AssertionError):
            serializer.save()
        after_count = User.objects.count()
        self.assertEqual(after_count, before_count)

    def test_email_must_have_before_at_symbol(self):
        """Test for the invalid serializer that can't be saved when the email has nothing before @"""

        self.serializer_data['email'] = '@example.org'
        serializer = SignUpSerializer(data=self.serializer_data)
        self.assertFalse(serializer.is_valid())
        before_count = User.objects.count()
        with self.assertRaises(AssertionError):
            serializer.save()
        after_count = User.objects.count()
        self.assertEqual(after_count, before_count)

    def test_email_must_have_at_symbol(self):
        """Test for the invalid serializer that can't be saved when the email has no @"""

        self.serializer_data['email'] = 'baldunicornexample.org'
        serializer = SignUpSerializer(data=self.serializer_data)
        self.assertFalse(serializer.is_valid())
        before_count = User.objects.count()
        with self.assertRaises(AssertionError):
            serializer.save()
        after_count = User.objects.count()
        self.assertEqual(after_count, before_count)

    def test_email_must_have_domain_name(self):
        """Test for the invalid serializer that can't be saved when the email has no domain name"""

        self.serializer_data['email'] = 'baldunicorn@.org'
        serializer = SignUpSerializer(data=self.serializer_data)
        self.assertFalse(serializer.is_valid())
        before_count = User.objects.count()
        with self.assertRaises(AssertionError):
            serializer.save()
        after_count = User.objects.count()
        self.assertEqual(after_count, before_count)

    def test_email_must_have_domain(self):
        """Test for the invalid serializer that can't be saved when the email has no domain"""

        self.serializer_data['email'] = 'baldunicorn@example'
        serializer = SignUpSerializer(data=self.serializer_data)
        self.assertFalse(serializer.is_valid())
        before_count = User.objects.count()
        with self.assertRaises(AssertionError):
            serializer.save()
        after_count = User.objects.count()
        self.assertEqual(after_count, before_count)

    def test_firstname_must_not_be_longer_50_characters(self):
        """Test for the invalid serializer that can't be saved when the firstname contains more than 50 characters."""

        self.serializer_data['first_name'] = 'b' * 51
        serializer = SignUpSerializer(data=self.serializer_data)
        self.assertFalse(serializer.is_valid())
        before_count = User.objects.count()
        with self.assertRaises(AssertionError):
            serializer.save()
        after_count = User.objects.count()
        self.assertEqual(after_count, before_count)

    def test_first_name_can_be_50_characters_(self):
        """Test for the invalid serializer that can be saved when the firstname contains 50 characterss."""

        self.serializer_data['first_name'] = 'b' * 50
        serializer = SignUpSerializer(data=self.serializer_data)
        self.assertTrue(serializer.is_valid())
        before_count = User.objects.count()
        serializer.save()
        after_count = User.objects.count()
        self.assertEqual(after_count, before_count+1)

    def test_first_name_can_be_3_characters(self):
        """Test for the invalid serializer that can be saved when the firstname contains 50 characters."""

        self.serializer_data['first_name'] = 'b' * 3
        serializer = SignUpSerializer(data=self.serializer_data)
        self.assertTrue(serializer.is_valid())
        before_count = User.objects.count()
        serializer.save()
        after_count = User.objects.count()
        self.assertEqual(after_count, before_count+1)

    def test_first_name_must_not_be_blank(self):
        """Test for the invalid serializer that can't be saved when the first_name is blank."""

        self.serializer_data['first_name'] = ''
        serializer = SignUpSerializer(data=self.serializer_data)
        self.assertFalse(serializer.is_valid())
        before_count = User.objects.count()
        with self.assertRaises(AssertionError):
            serializer.save()
        after_count = User.objects.count()
        self.assertEqual(after_count, before_count)

    def test_lastname_must_not_be_longer_50_characters(self):
        """Test for the invalid serializer that can't be saved when the lastname contains more than 50 characters."""

        self.serializer_data['last_name'] = 'b' * 51
        serializer = SignUpSerializer(data=self.serializer_data)
        self.assertFalse(serializer.is_valid())
        before_count = User.objects.count()
        with self.assertRaises(AssertionError):
            serializer.save()
        after_count = User.objects.count()
        self.assertEqual(after_count, before_count)

    def test_last_name_can_be_50_characters_(self):
        """Test for the invalid serializer that can be saved when the lastname contains 50 characterss."""

        self.serializer_data['last_name'] = 'b' * 50
        serializer = SignUpSerializer(data=self.serializer_data)
        self.assertTrue(serializer.is_valid())
        before_count = User.objects.count()
        serializer.save()
        after_count = User.objects.count()
        self.assertEqual(after_count, before_count+1)

    def test_last_name_can_be_3_characters(self):
        """Test for the invalid serializer that can be saved when the lastname contains 50 characters."""

        self.serializer_data['last_name'] = 'b' * 3
        serializer = SignUpSerializer(data=self.serializer_data)
        self.assertTrue(serializer.is_valid())
        before_count = User.objects.count()
        serializer.save()
        after_count = User.objects.count()
        self.assertEqual(after_count, before_count+1)

    def test_last_name_must_not_be_blank(self):
        """Test for the invalid serializer that can't be saved when the last_name is blank."""

        self.serializer_data['last_name'] = ''
        serializer = SignUpSerializer(data=self.serializer_data)
        self.assertFalse(serializer.is_valid())
        before_count = User.objects.count()
        with self.assertRaises(AssertionError):
            serializer.save()
        after_count = User.objects.count()
        self.assertEqual(after_count, before_count)

    def test_bio_can_be_500_characters_(self):
        """Test for the invalid serializer that can be saved when the bio contains 500 characterss."""

        self.serializer_data['bio'] = 'b' * 500
        serializer = SignUpSerializer(data=self.serializer_data)
        self.assertTrue(serializer.is_valid())
        before_count = User.objects.count()
        serializer.save()
        after_count = User.objects.count()
        self.assertEqual(after_count, before_count+1)

    def test_bio_can_be_3_characters(self):
        """Test for the invalid serializer that can be saved when the bio contains 3 characters."""

        self.serializer_data['bio'] = 'b' * 3
        serializer = SignUpSerializer(data=self.serializer_data)
        self.assertTrue(serializer.is_valid())
        before_count = User.objects.count()
        serializer.save()
        after_count = User.objects.count()
        self.assertEqual(after_count, before_count+1)

    def test_bio_cannnot_be_501_characters(self):
        """Test for the invalid serializer that can be saved when the bio 501 characters."""

        self.serializer_data['bio'] = 'b' * 501
        serializer = SignUpSerializer(data=self.serializer_data)
        self.assertFalse(serializer.is_valid())
        before_count = User.objects.count()
        with self.assertRaises(AssertionError):
            serializer.save()
        after_count = User.objects.count()
        self.assertEqual(after_count, before_count)

    def test_bio_can_be_blank(self):
        """Test for the invalid serializer that can be saved when the bio is blank."""

        self.serializer_data['bio'] = ''
        serializer = SignUpSerializer(data=self.serializer_data)
        self.assertTrue(serializer.is_valid())
        before_count = User.objects.count()
        serializer.save()
        after_count = User.objects.count()
        self.assertEqual(after_count, before_count+1)
