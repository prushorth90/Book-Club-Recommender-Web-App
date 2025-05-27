from django.urls import path
from .views import index

urlpatterns = [
    path('', index),
    path('create/', index),
    path('login/', index),
    path('signup/', index),
    path('club/<str:name>', index),
    path('edit-club/<str:name>',index),
    path('delete-club/<str:name>',index),
    path('logout', index),
    path('dashboard', index),
    path('join_club', index),
    path('create-post/<str:name>', index),
    path('member_list/<int:id>', index),
    path('applicant_list/<int:id>', index),
    path('create_meeting/<int:id>', index),
    path('meeting_list', index),
    path('show_member', index),
    path('show_meeting/<int:id>', index),
    path('update_meeting/<int:id>', index),
    path('update_profile/', index),
    path('my_clubs', index),
    path('update_password', index),
    path('rightbar', index),
    path('rate_books', index),
    path('club/<int:id>/chat-room',index)
]