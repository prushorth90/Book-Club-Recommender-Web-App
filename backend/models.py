"""Models for the bookaholics app."""
from django.db import models
from django.contrib.auth.models import AbstractUser
from django.core.validators import RegexValidator, MaxValueValidator, MinValueValidator
from libgravatar import Gravatar
from profanity.validators import validate_is_profane
import datetime

class User(AbstractUser):
    """User model for authentication."""

    username = models.CharField(
        max_length=50,
        unique=True,
        blank=False,
        validators=[RegexValidator(
            regex=r'^\w{3,}$',
            message='Username must have at least three alphanumericals'
        )]
    )
    email = models.EmailField(unique=True, blank=False)
    first_name = models.CharField(max_length=50, unique=False, blank=False)
    last_name = models.CharField(max_length=50, unique=False, blank=False)
    bio = models.CharField(max_length=500, unique=False, blank=True)

    def gravatar(self, size=100):
        """Return a URL to the user's gravatar."""

        gravatar = Gravatar(self.email)
        gravatar_url = gravatar.get_image(size=size, default='mp')
        return gravatar_url

    def mini_gravatar(self):
        """Return a URL to a smaller version of user's gravatar."""

        return self.gravatar(size=50)

class Club(models.Model):
    """Clubs created by users in book club."""

    name = models.CharField(max_length=50, unique=True, blank=False)
    description = models.CharField(max_length=500, blank=False)
    members_capacity = models.PositiveSmallIntegerField(
        blank=False,
        default=50,
        validators=[
            MaxValueValidator(
                limit_value=50,
                message='The maximum members capacity is 50'
            ),
            MinValueValidator(
                limit_value=2,
                message='The minimum number of members in a club is 2'
            )
        ]
    )

    def __str__(self):
        return self.name

class User_Auth(models.Model):
    """Authorization for each member of a club."""

    rank = models.CharField(
        choices=[
            ('applicant', 'Applicant'),
            ('member', 'Member'),
            ('owner', 'Owner')
        ],
        max_length=9,
        default='applicant'
    )
    club = models.ForeignKey(Club, on_delete=models.CASCADE, blank=False, null=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE, blank=False, null=True)

    class Meta:
        unique_together = (("user", "club"),)

class Post(models.Model):
    """The post created by a member of a club which can only be seen by the members in the same club."""

    author = models.ForeignKey(User, on_delete=models.CASCADE, blank=False)
    text = models.CharField(max_length=280, blank=False)
    created_at = models.DateTimeField(auto_now_add=True)
    club = models.ForeignKey(Club, on_delete=models.CASCADE, blank=False)

    class Meta:
        ordering = ['-created_at']

class Book(models.Model):
    """The book model which contains the book's details."""

    isbn = models.CharField(max_length=13, unique=True, blank=False)
    title = models.TextField(unique=False, blank=False)
    image_url = models.URLField(max_length=3000, unique=False, blank=True)

    def __str__(self):
        return self.title

class Meeting(models.Model):
    """Meeting created by user in a club to discuss about a book."""

    club = models.ForeignKey(Club, on_delete=models.CASCADE, blank=False)
    creator = models.ForeignKey(User, on_delete=models.CASCADE, blank=False, null=True)
    date = models.DateField(
        null=True,
        validators=[MinValueValidator(
            limit_value=datetime.date.today,
            message="The date must be today's date or any future date"
        )]
    )
    time = models.TimeField(blank=False)
    book = models.ForeignKey(Book, on_delete=models.SET_NULL, blank=False, null=True)
    location = models.CharField(max_length=300, unique=False, blank=False)
    link_to_meeting = models.URLField(max_length=2500, unique=False, blank=True)
    remote = models.BooleanField(default=False)
    isEnd = models.BooleanField(default=False)

    class Meta:
        unique_together = (("club","date","time"))

class BookRating(models.Model):
    """A rating of a book created by a user."""

    creator = models.ForeignKey(User, on_delete=models.CASCADE, blank=False, null = True)
    book = models.ForeignKey(Book, on_delete=models.SET_NULL, null=True)
    rating = models.PositiveSmallIntegerField(
        blank=False,
        default=1,
        validators=[
            MaxValueValidator(
                limit_value=10,
                message='The maximum members capacity is 10'
            ),
            MinValueValidator(
                limit_value=1,
                message='The minimum number of members in a club is 1'
            )
        ]
    )
    def __str__(self):
        return self.title

class ChatRoom(models.Model):
    """A room to allow members to chat with each other in the club."""

    club = models.ForeignKey(Club, on_delete=models.CASCADE, related_name='club')
    name = models.CharField(max_length=255)
    created_by = models.ForeignKey(User, on_delete=models.CASCADE, related_name='my_chat_rooms')
    members = models.ManyToManyField(User, related_name='chats')
    timestamp = models.DateTimeField(auto_now_add=True)

class Message(models.Model):
    """A message sent by a user in the chat room."""

    chat_room = models.ForeignKey(ChatRoom, on_delete=models.CASCADE)
    created_by = models.ForeignKey(User, on_delete=models.CASCADE, related_name='my_messages')
    message = models.TextField(validators=[validate_is_profane])
    timestamp = models.DateTimeField(auto_now_add=True)
    def __str__(self):
        return self.message
