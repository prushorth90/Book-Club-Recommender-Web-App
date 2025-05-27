"""Unit tests for club serializer."""
from unibook.models import Club
from unibook.serializers import ClubSerializer
from rest_framework.test import APITestCase

class ClubSerializerTestCase(APITestCase):
    """Unit tests for club serializer."""

    def setUp(self):
        self.serializer_data = {
            'name': 'Uniclub',
            'description': 'A club for people that falls asleep while reading books.',
            'members_capacity': 50
        }

    def test_valid_club_serializer(self):
        """Test the serializer to create a valid club."""

        serializer = ClubSerializer(data=self.serializer_data)
        self.assertTrue(serializer.is_valid())

    def test_serializer_has_necessary_fields(self):
        """Test the serializer to check if it has necessary fields."""

        serializer = ClubSerializer()
        self.assertIn('name', serializer.fields)
        self.assertIn('description', serializer.fields)
        self.assertIn('members_capacity', serializer.fields)

    def test_serializer_saves_correctly(self):
        """Test that the serializer saves correctly."""

        serializer = ClubSerializer(data=self.serializer_data)
        before_count = Club.objects.count()
        serializer.is_valid()
        serializer.save()
        after_count = Club.objects.count()
        self.assertEqual(after_count, before_count + 1)
        club = Club.objects.get(name='Uniclub')
        self.assertEqual(club.name, 'Uniclub')
        self.assertEqual(club.description, 'A club for people that falls asleep while reading books.')
        self.assertEqual(club.members_capacity, 50)

    def test_name_must_contain_at_most_50_characters(self):
        """Test for the invalid serializer that can't be saved when the name contains more than 50 characters."""

        self.serializer_data['name'] = 'n' * 51
        serializer = ClubSerializer(data=self.serializer_data)
        self.assertFalse(serializer.is_valid())
        before_count = Club.objects.count()
        with self.assertRaises(AssertionError):
            serializer.save()
        after_count = Club.objects.count()
        self.assertEqual(after_count, before_count)

    def test_name_must_not_be_blank(self):
        """Test for the invalid serializer that can't be saved when the name is blank."""

        self.serializer_data['name'] = ''
        serializer = ClubSerializer(data=self.serializer_data)
        self.assertFalse(serializer.is_valid())
        before_count = Club.objects.count()
        with self.assertRaises(AssertionError):
            serializer.save()
        after_count = Club.objects.count()
        self.assertEqual(after_count, before_count)

    def test_description_must_contain_at_most_500_characters(self):
        """Test for the invalid serializer that can't be saved when the description contains more than 500 characters."""

        self.serializer_data['description'] = 'd' * 501
        serializer = ClubSerializer(data=self.serializer_data)
        self.assertFalse(serializer.is_valid())
        before_count = Club.objects.count()
        with self.assertRaises(AssertionError):
            serializer.save()
        after_count = Club.objects.count()
        self.assertEqual(after_count, before_count)

    def test_description_must_not_be_blank(self):
        """Test for the invalid serializer that can't be saved when the description is blank."""

        self.serializer_data['description'] = ''
        serializer = ClubSerializer(data=self.serializer_data)
        self.assertFalse(serializer.is_valid())
        before_count = Club.objects.count()
        with self.assertRaises(AssertionError):
            serializer.save()
        after_count = Club.objects.count()
        self.assertEqual(after_count, before_count)

    def test_members_capacity_must_be_at_most_50(self):
        """Test for the invalid serializer that can't be saved when the members capacity is more than 50."""

        self.serializer_data['members_capacity'] = 51
        serializer = ClubSerializer(data=self.serializer_data)
        self.assertFalse(serializer.is_valid())
        before_count = Club.objects.count()
        with self.assertRaises(AssertionError):
            serializer.save()
        after_count = Club.objects.count()
        self.assertEqual(after_count, before_count)

    def test_members_capacity_must_be_at_least_2(self):
        """Test for the invalid serializer that can't be saved when the members capacity is less than 2."""

        self.serializer_data['members_capacity'] = 1
        serializer = ClubSerializer(data=self.serializer_data)
        self.assertFalse(serializer.is_valid())
        before_count = Club.objects.count()
        with self.assertRaises(AssertionError):
            serializer.save()
        after_count = Club.objects.count()
        self.assertEqual(after_count, before_count)
