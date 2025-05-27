""" Unit tests for update user serializer """
from unibook.models import User
from unibook.serializers import UpdateUserSerializer
from rest_framework.test import APITestCase

class UpdateUserSerializerTestCase(APITestCase):
    """Unit tests for update user serializer."""

    fixtures = [
        'unibook/tests/fixtures/default_user.json',
        'unibook/tests/fixtures/other_users.json'
    ]

    def setUp(self):
        self.user = User.objects.get(username='baldunicorn')
        self.other_user = User.objects.get(username='fluffyunicorn')

        self.serializer_data = {
          'username': 'smarthorse',
          'first_name': 'Smart',
          'last_name': 'Horse',
          'email': 'smarthorse@example.org',
          'bio': 'I AM NOT BALD ANYMORE!',
        }

    def test_valid_update_user_serializer(self):
        """Test the serializer to update a valid user's details."""

        serializer = UpdateUserSerializer(data=self.serializer_data)
        self.assertTrue(serializer.is_valid())

    def test_serializer_has_necessary_fields(self):
        """Test the serializer to check if it has necessary fields."""

        serializer = UpdateUserSerializer()
        self.assertIn('username', serializer.fields)
        self.assertIn('first_name', serializer.fields)
        self.assertIn('last_name', serializer.fields)
        self.assertIn('email', serializer.fields)
        self.assertIn('bio', serializer.fields)

    def test_serializer_updates_correctly(self):
        """Test that the serializer updates correctly."""

        serializer = UpdateUserSerializer(instance=self.user, data=self.serializer_data)
        before_count = User.objects.count()
        serializer.is_valid()
        instance = serializer.update(self.user, self.serializer_data)
        after_count = User.objects.count()
        self.assertEqual(after_count, before_count)

        self.assertEqual(self.user.username, 'smarthorse')
        self.assertEqual(self.user.first_name, 'Smart')
        self.assertEqual(self.user.last_name, 'Horse')
        self.assertEqual(self.user.email, 'smarthorse@example.org')
        self.assertEqual(self.user.bio, 'I AM NOT BALD ANYMORE!')

    """ Unit test for username """

    def test_username_must_not_be_longer_50_characters(self):
        invalid_username = 's' * 51
        self.serializer_data['username'] = invalid_username
        serializer = UpdateUserSerializer(instance=self.user, data=self.serializer_data)
        self.assertFalse(serializer.is_valid())

    def test_username_can_be_50_characters_(self):
        new_username = 's' * 50
        self.serializer_data['username'] = new_username
        serializer = UpdateUserSerializer(instance=self.user, data=self.serializer_data)
        self.assertTrue(serializer.is_valid())
        before_count = User.objects.count()
        serializer.update(self.user, self.serializer_data)
        self.assertEqual(self.user.username, new_username)
        after_count = User.objects.count()
        self.assertEqual(after_count, before_count)

    def test_username_can_be_3_characters(self):
        new_username = 's' * 3
        self.serializer_data['username'] = new_username
        serializer = UpdateUserSerializer(instance=self.user, data=self.serializer_data)
        self.assertTrue(serializer.is_valid())
        before_count = User.objects.count()
        serializer.update(self.user, self.serializer_data)
        self.assertEqual(self.user.username, new_username)
        after_count = User.objects.count()
        self.assertEqual(after_count, before_count)

    def test_username_can_between_3_and_50_characters(self):
        new_username = 's' * 9
        self.serializer_data['username'] = new_username
        serializer = UpdateUserSerializer(instance=self.user, data=self.serializer_data)
        self.assertTrue(serializer.is_valid())
        before_count = User.objects.count()
        serializer.update(self.user, self.serializer_data)
        self.assertEqual(self.user.username, new_username)
        after_count = User.objects.count()
        self.assertEqual(after_count, before_count)

    def test_username_cannot_be_2_characters(self):
        self.serializer_data['username'] = 's' * 2
        serializer = UpdateUserSerializer(instance=self.user, data=self.serializer_data)
        self.assertFalse(serializer.is_valid())

    def test_username_must_not_be_blank(self):
        self.serializer_data['username'] = ''
        serializer = UpdateUserSerializer(instance=self.user, data=self.serializer_data)
        self.assertFalse(serializer.is_valid())

    def test_username_must_not_be_taken(self):
        self.serializer_data['username'] = self.other_user.username
        serializer = UpdateUserSerializer(instance=self.user, data=self.serializer_data)
        self.assertFalse(serializer.is_valid())

    """ Unit test for email """

    def test_email_must_not_be_blank(self):
        self.serializer_data['email'] = ''
        serializer = UpdateUserSerializer(instance=self.user, data=self.serializer_data)
        self.assertFalse(serializer.is_valid())

    def test_email_must_have_before_at_symbol(self):
        self.serializer_data['email'] = '@example.org'
        serializer = UpdateUserSerializer(instance=self.user, data=self.serializer_data)
        self.assertFalse(serializer.is_valid())

    def test_email_must_have_at_symbol(self):
        self.serializer_data['email'] = 'smarthorseexample.org'
        serializer = UpdateUserSerializer(instance=self.user, data=self.serializer_data)
        self.assertFalse(serializer.is_valid())

    def test_email_must_have_domain_name(self):
        self.serializer_data['email'] = 'smarthorse@.org'
        serializer = UpdateUserSerializer(instance=self.user, data=self.serializer_data)
        self.assertFalse(serializer.is_valid())

    def test_email_must_have_domain(self):
        self.serializer_data['email'] = 'smarthorse@example'
        serializer = UpdateUserSerializer(instance=self.user, data=self.serializer_data)
        self.assertFalse(serializer.is_valid())

    """ Unit test for firstname """

    def test_firstname_must_not_be_longer_50_characters(self):
        self.serializer_data['first_name'] = 's' * 51
        serializer = UpdateUserSerializer(instance=self.user, data=self.serializer_data)
        self.assertFalse(serializer.is_valid())

    def test_first_name_can_be_50_characters_(self):
        new_first_name = 's' * 50
        self.serializer_data['first_name'] = new_first_name
        serializer = UpdateUserSerializer(instance=self.user, data=self.serializer_data)
        self.assertTrue(serializer.is_valid())
        before_count = User.objects.count()
        serializer.update(self.user, self.serializer_data)
        self.assertEqual(self.user.first_name, new_first_name)
        after_count = User.objects.count()
        self.assertEqual(after_count, before_count)

    def test_first_name_can_be_3_characters(self):
        new_first_name = 's' * 3
        self.serializer_data['first_name'] = new_first_name
        serializer = UpdateUserSerializer(instance=self.user, data=self.serializer_data)
        self.assertTrue(serializer.is_valid())
        before_count = User.objects.count()
        serializer.update(self.user, self.serializer_data)
        self.assertEqual(self.user.first_name, new_first_name)
        after_count = User.objects.count()
        self.assertEqual(after_count, before_count)

    def test_first_name_must_not_be_blank(self):
        self.serializer_data['first_name'] = ''
        serializer = UpdateUserSerializer(instance=self.user, data=self.serializer_data)
        self.assertFalse(serializer.is_valid())

    """ Unit test for lastname """

    def test_lastname_must_not_be_longer_50_characters(self):
        self.serializer_data['last_name'] = 'h' * 51
        serializer = UpdateUserSerializer(instance=self.user, data=self.serializer_data)
        self.assertFalse(serializer.is_valid())

    def test_last_name_can_be_50_characters_(self):
        new_last_name = 'h' * 50
        self.serializer_data['last_name'] = new_last_name
        serializer = UpdateUserSerializer(instance=self.user, data=self.serializer_data)
        self.assertTrue(serializer.is_valid())
        before_count = User.objects.count()
        serializer.update(self.user, self.serializer_data)
        self.assertEqual(self.user.last_name, new_last_name)
        after_count = User.objects.count()
        self.assertEqual(after_count, before_count)

    def test_last_name_can_be_3_characters(self):
        new_last_name = 'h' * 3
        self.serializer_data['last_name'] = new_last_name
        serializer = UpdateUserSerializer(instance=self.user, data=self.serializer_data)
        self.assertTrue(serializer.is_valid())
        before_count = User.objects.count()
        serializer.update(self.user, self.serializer_data)
        self.assertEqual(self.user.last_name, new_last_name)
        after_count = User.objects.count()
        self.assertEqual(after_count, before_count)

    def test_last_name_must_not_be_blank(self):
        self.serializer_data['last_name'] = ''
        serializer = UpdateUserSerializer(instance=self.user, data=self.serializer_data)
        self.assertFalse(serializer.is_valid())

    """ Unit test for bio """

    def test_bio_can_be_500_characters_(self):
        new_bio = 'b' * 500
        self.serializer_data['bio'] = new_bio
        serializer = UpdateUserSerializer(instance=self.user, data=self.serializer_data)
        self.assertTrue(serializer.is_valid())
        before_count = User.objects.count()
        serializer.update(self.user, self.serializer_data)
        self.assertEqual(self.user.bio, new_bio)
        after_count = User.objects.count()
        self.assertEqual(after_count, before_count)

    def test_bio_can_be_3_characters(self):
        new_bio = 'b' * 3
        self.serializer_data['bio'] = new_bio
        serializer = UpdateUserSerializer(instance=self.user, data=self.serializer_data)
        self.assertTrue(serializer.is_valid())
        before_count = User.objects.count()
        serializer.update(self.user, self.serializer_data)
        self.assertEqual(self.user.bio, new_bio)
        after_count = User.objects.count()
        self.assertEqual(after_count, before_count)

    def test_bio_cannnot_be_501_characters(self):
        self.serializer_data['bio'] = 'b' * 501
        serializer = UpdateUserSerializer(instance=self.user, data=self.serializer_data)
        self.assertFalse(serializer.is_valid())

    def test_bio_can_be_blank(self):
        new_bio = ''
        self.serializer_data['bio'] = new_bio
        serializer = UpdateUserSerializer(instance=self.user, data=self.serializer_data)
        self.assertTrue(serializer.is_valid())
        before_count = User.objects.count()
        serializer.update(self.user, self.serializer_data)
        self.assertEqual(self.user.bio, new_bio)
        after_count = User.objects.count()
        self.assertEqual(after_count, before_count)
