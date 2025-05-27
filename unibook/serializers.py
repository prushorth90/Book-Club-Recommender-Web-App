from rest_framework import serializers
import re
from .models import BookRating, User, Club, Post, Meeting, User_Auth, Book, ChatRoom, Message

from .models import BookRating, User, Club, Post, Meeting, User_Auth, Book
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer

class MyTokenObtainPairSerializer(TokenObtainPairSerializer):
    @classmethod
    def get_token(cls, user):
        token = super().get_token(user)
        token['username'] = user.username

        return token

# User Serializer
class UserSerializer(serializers.ModelSerializer):
    """Serializer for user's details."""

    class Meta:
        model = User
        fields = ['id', 'first_name', 'last_name', 'username', 'email', 'bio', 'password']
        extra_kwargs = {'password': {'write_only': True}}


# SignUp Serializer
class SignUpSerializer(serializers.ModelSerializer):
    """Serializer to let user sign up."""

    class Meta:
        model = User
        fields = ['first_name', 'last_name', 'username', 'email', 'bio', 'password',]
        extra_kwargs = {'password': {'write_only': True}}

    def create(self, validated_data):
        """Create the user."""

        password = validated_data.pop('password', None)
        instance = self.Meta.model(**validated_data)
        if password is not None:
            instance.set_password(password)
        instance.save()
        return instance

class ChangePasswordSerializer(serializers.Serializer):
    """Serializer to update user's password."""

    model = User

    old_password = serializers.CharField(required=True)
    new_password = serializers.CharField(required=True)

    def validate_new_password(self, value):
        """Validate if the new password contain an uppercase character, a lowercase character and a number"""

        regex=r'^(?=.*[A-Z])(?=.*[a-z])(?=.*[0-9]).*$'
        if (not re.match(regex, value)):
            raise serializers.ValidationError('Password must contain an uppercase character, a lowercase character and a number')

class UpdateUserSerializer(serializers.ModelSerializer):
    """Serializer to update a user's details."""

    email = serializers.EmailField(required=True)

    class Meta:
        model = User
        fields = ['username', 'first_name', 'last_name', 'email', 'bio']
        extra_kwargs = {
            'first_name': {'required': True},
            'last_name': {'required': True},
        }

        def validate_email(self, value):
            """Check if the email is taken."""

            user = self.context['request'].user
            if User.objects.exclude(pk=user.pk).filter(email=value).exists():
                raise serializers.ValidationError({"email": "This email is already in use."})
            return value

        def validate_username(self, value):
            """Check if the username is taken."""

            user = self.context['request'].user
            if User.objects.exclude(pk=user.pk).filter(username=value).exists():
                raise serializers.ValidationError({"username": "This username is already in use."})
            return value

        def update(self, instance, validated_data):
            """Update the user's details."""

            user = self.context['request'].user

            if user.pk != instance.pk:
                raise serializers.ValidationError({"authorize": "You dont have permission for this user."})

            instance.first_name = validated_data['first_name']
            instance.last_name = validated_data['last_name']
            instance.email = validated_data['email']
            instance.username = validated_data['username']
            instance.bio = validated_data['bio']

            instance.save()

            return instance

class ClubSerializer(serializers.ModelSerializer):
    """Serializer for a club."""

    class Meta:
        model = Club
        fields = ['id','name', 'description','members_capacity']

class UserAuthSerializer(serializers.ModelSerializer):
    """Serializer for the user authorization of a user."""

    club = serializers.SlugRelatedField(slug_field='name' ,queryset=Club.objects.all())
    user = serializers.SlugRelatedField(slug_field='username' ,queryset=User.objects.all())
    class Meta:
        model = User_Auth
        fields = ['id', 'rank', 'club', 'user']

class PostSerializer(serializers.ModelSerializer):
    """Serializer for post in a club."""

    club = serializers.SlugRelatedField(slug_field='name' ,queryset=Club.objects.all())
    author = serializers.SlugRelatedField(slug_field='username' ,queryset=User.objects.all())
    class Meta:
        model = Post
        fields = ['id', 'text', 'created_at', 'club', 'author']

class MeetingSerializer(serializers.ModelSerializer):
    """Serializer for a meeting in the club."""

    club = serializers.SlugRelatedField(slug_field='id' ,queryset=Club.objects.all())
    creator = serializers.SlugRelatedField(slug_field='username' ,queryset=User.objects.all())
    book = serializers.SlugRelatedField(slug_field='isbn', queryset=Book.objects.all())

    class Meta:
        model = Meeting
        fields = ['id', 'club', 'creator', 'date', 'time', 'book', 'location', 'link_to_meeting', 'remote']

class BookRatingSerializer(serializers.ModelSerializer):
    # book = autocomplete.ModelSelect2(url='book-autocomplete'),
    book = serializers.SlugRelatedField(slug_field='isbn', queryset=Book.objects.all())

    class Meta:
        model = BookRating
        fields = ['book', 'rating']

class BookSerializer(serializers.ModelSerializer):
    """Serializer to create a book."""

    class Meta:
        model = Book
        fields = ['isbn', 'title', 'image_url']

class UpdateMeetingSerializer(serializers.ModelSerializer):
    """Serializer to update a meeting in the club."""

    class Meta:
        model = Meeting
        fields = ('id', 'date', 'time', 'book', 'location', 'link_to_meeting')
        extra_kwargs = {
            'date': {'required': True},
            'time': {'required': True},
            'book': {'required': True},
            'location': {'required': True},
            'link_to_meeting': {'required': True},
        }

        def update(self, instance, validated_data):
            """Update the meeting's details."""

            meeting = self.context['request'].meeting

            if meeting.pk != instance.pk:
                raise serializers.ValidationError({"authorize": "You dont have permission for this user."})

            instance.date = validated_data['date']
            instance.time = validated_data['time']
            instance.book = validated_data['book']
            instance.location = validated_data['location']
            instance.link_to_meeting = validated_data['link_to_meeting']

            instance.save()

            return instance

        fields = ['creator', 'date', 'time', 'book', 'location', 'link_to_meeting', 'remote']

class ChatRoomSerializer(serializers.ModelSerializer):
    class Meta:
        model = ChatRoom
        fields = '__all__'
    # POST {'club': 123, 'name': 'My Cool chatroom', 'created_by': 1232, members: [123,432,123]}

# Message Serializer
class MessageSerializer(serializers.ModelSerializer):
    chat_room = serializers.SlugRelatedField(slug_field='id' ,queryset=ChatRoom.objects.all())
    created_by = serializers.SlugRelatedField(slug_field='id' ,queryset=User.objects.all())

    """For Serializing Message"""
    class Meta:
        model = Message
        fields = ['chat_room', 'message', 'timestamp', 'created_by']
