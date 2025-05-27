"""Django-admin page"""
from unibook.models import User, User_Auth, Club,Meeting, Post, Book, ChatRoom, Message
from django.contrib import admin

@admin.register(User)
class UserAdmin(admin.ModelAdmin):
    """Configuration of the admin interface for users."""

    list_display = (
        'username', 'email', 'first_name', 'last_name',
    )

@admin.register(User_Auth)
class UserAuthAdmin(admin.ModelAdmin):
    """Configuration of the admin interface for user auth."""

    list_display = (
        'user','rank','club',
    )

@admin.register(Club)
class ClubAdmin(admin.ModelAdmin):
    """Configuration of the admin interface for clubs."""

    list_display = (
        'id', 'name', 'description',
    )

@admin.register(Meeting)
class MeetingAdmin(admin.ModelAdmin):
    """Configuration of the admin interface for meetings."""

    list_display = (
        'id', 'club', 'date', 'time', 'location', 'book'
    )
    raw_id_fields = ['book']


@admin.register(Book)
class BookAdmin(admin.ModelAdmin):
    """Configuration of the admin interface for books."""

    list_display = ['id', 'isbn', 'title', 'image_url']
    search_fields = ['title', 'isbn']

@admin.register(ChatRoom)
class ChatRoomAdmin(admin.ModelAdmin):
    """Configuration of the admin interface for chatrooms."""

    list_display = (
        'club', 'name', 'created_by', 'timestamp'
    )

@admin.register(Message)
class MessageAdmin(admin.ModelAdmin):
    """Configuration of the admin interface for messages in a chatroom."""

    list_display = (
        'chat_room', 'created_by', 'message', 'timestamp'
    )
