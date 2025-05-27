"""bookClub URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path, include
from unibook import views
from rest_framework_simplejwt.views import (
    TokenObtainPairView,
    TokenRefreshView,
)

urlpatterns = [
    path('admin/', admin.site.urls),
    path('unibook/', include('unibook.urls')),
    path('', include('frontend.urls')),
    path('api-auth/', include('rest_framework.urls', namespace='rest_framework')),
    # path('unibook/token/obtain/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('unibook/token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),


    # path(
    #     'book-autocomplete/',
    #     views.BookAutocomplete.as_view(),
    #     name='book-autocomplete',
    # ),
    
    #path('dashboard/', views.dashboard, name='dashboard'),
    #path('delete_account/', views.delete_account, name='delete_account'),
    #path('log_out/', views.log_out, name='log_out'),
    #path('log_in/', views.log_in, name='log_in'),
    #path('sign_up/', views.sign_up, name='sign_up'),
    #path('password/', views.password, name='password'),
    #path('create_club/', views.create_club, name='create_club'),
    #path('my_clubs/', views.my_clubs, name='my_clubs'),
    #path('other_clubs/', views.other_clubs, name='other_clubs'),
    #path('show_club/<int:club_id>', views.show_club, name='show_club'),
    #path('delete_club/<int:club_id>', views.delete_club, name='delete_club'),
    #path('new_post/', views.new_post, name='new_post'),
    #path('apply_club/<int:club_id>', views.apply_club, name='apply_club'),
    #path('create_meeting/<int:club_id>',views.create_meeting, name='create_meeting'),
    #path('member_list/<int:club_id>',views.member_list, name='member_list'),
    #path('<int:club_id>/show_member/<int:member_id>', views.show_member, name='show_member'),
    #path('<int:club_id>/transfer_ownership/<int:member_id>',views.transfer_ownership, name='transfer_ownership'),
    #path('update_profile/', views.update_profile, name='update_profile'),
    #path('meeting_list/<int:club_id>',views.meeting_list, name='meeting_list'),
    #path('<int:club_id>/show_meeting/<int:meeting_id>', views.show_meeting, name='show_meeting'),
    #path('<int:club_id>/delete_meeting/<int:meeting_id>', views.delete_meeting, name='delete_meeting'),
    #path('<int:club_id>/remove_member/<int:member_id>', views.remove_member, name='remove_member'),
    #path('<int:club_id>/update_meeting/<int:meeting_id>', views.update_meeting, name='update_meeting'),
]
