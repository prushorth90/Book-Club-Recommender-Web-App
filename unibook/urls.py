"""bookClub URL Configuation"""
from distutils.log import Log
from django.urls import path
from .views import *
from rest_framework import routers

router = routers.SimpleRouter()
router.register(r'club/<int:club_id>/chat-room', ChatRoomViewSet, basename='chat_room')
router.register(r'messages', MessageViewSet)


urlpatterns = [
    path('signup/', SignUpView.as_view(), name='signup'),
    path('logout/blacklist/', LogoutAndBlackListTokenView.as_view(), name='log_out'),
    path('change-password/',ChangePasswordView.as_view(), name='change_password'),
    path('token/obtain/', MyTokenObtainPairView.as_view(), name='token_obtain_pair'),

    #Recommender URLS
    path('user-recommendations/',UserRecommenderView.as_view(),name='user_recommender'),
    path('book_rating/', CreateBookRatings.as_view(), name='book_ratings'),
    path('get_rated_books/', GetBooksToShow.as_view(), name='get_rated_book'),
    path('book-list/',ListBooks.as_view(),name='book_list'),
    path('club-recommendations/<int:club_id>/', ClubRecommenderView.as_view(), name='club_recommender'),

    #User URLS
    path('user-list/', UserList.as_view(), name='user_list'),
    path('user-detail/<str:username>/', UserDetail.as_view(), name='user_detail'),
    path('edit-user/<str:username>/',EditUser.as_view(), name='edit_user'),
    path('current-user/', CurrentUserView.as_view(), name='current_user'),

    # Club URLS
    path('other-clubs-list/', ClubList.as_view(), name='other_club_list'),
    path('my-clubs-list/', MyClubList.as_view(), name='my_club_list'),
    # path('club-detail/<int:pk>/', ClubDetail.as_view(), name='club_detail'),
    path('club-detail/<int:club_id>/', ClubDetail.as_view(), name='club_detail'),
    path('create-club/', CreateClub.as_view(), name='create_club'),
    path('edit-club/<int:club_id>/', EditClub.as_view(), name='edit_club'),
    path('delete-club/<int:club_id>/', DeleteClub.as_view(), name='delete_club'),
    path('list-club-posts/<int:club_id>/', ListClubPostsView.as_view(), name='club_posts'),

    path('applicant-list/<int:club_id>/', ApplicantList.as_view(), name='applicant_list'),
    path('member-list/<int:club_id>/', MemberList.as_view(), name='member_list'),
    path('owner-list/<int:club_id>/', OwnerList.as_view(), name='owner_list'),
    path('update-user-auth/<int:auth_id>/', UpdateUserAuth.as_view()),
    path('leave-club/<int:club_id>/', LeaveClubView.as_view(), name='leave_club'),

    #User Auth URLS
    path('user-auth-detail/<int:club_id>/', UserAuthDetail.as_view(), name='user_auth_detail'),
    path('create-user-auth/', CreateUserAuth.as_view(), name='create_user_auth'),
    path('accept-user/<int:auth_id>/', AcceptApplication.as_view(), name='accept_user'),
    path('remove-user/<int:auth_id>', RemoveUserFromClub.as_view(), name='remove_user'),
    path('get-owner/<int:club_id>/', getOwner.as_view()),

    # Post URLS
    path('create-post/<int:club_id>', CreatePostView.as_view(), name='create_post'),
    path('edit-post/<int:post_id>', EditPostView.as_view(), name='edit_post'),
    path('delete-post/<int:post_id>', DeletePostView.as_view(), name='delete_post'),

    #Meeting URLS
    # path('my_meetings/<int:user_id>/', MyMeetings.as_view(), name='my_meetings'),
    path('create-meeting/<int:club_id>/', CreateMeetingView.as_view(), name='create_meeting'),
    path('meeting-detail/<int:club_id>/', ClubMeetingDetail.as_view(), name='meeting_detail'),
    path('show-edit-meeting/<int:id>/', ShowEditMeeting.as_view(), name='show_edit_meeting'),
    path('edit-meeting/<int:id>/', EditMeetingView.as_view(), name='edit_meeting'),
    # path('list-club-meetings/<str:club>/', ListClubMeetings.as_view()),
    path('meeting-list/<int:club_id>/', MeetingListView.as_view(), name='meeting_list'),
    path('delete-meeting/<str:meeting_id>', DeleteMeetingView.as_view(), name='delete_meeting')
] + router.urls
