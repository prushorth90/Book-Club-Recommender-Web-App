from django.shortcuts import render,redirect
from numpy import True_
from unibook.orm_helper.orm_club import *
from unibook.orm_helper.orm_user import *
from unibook.orm_helper.orm_book import *
from django.contrib.auth.decorators import login_required
from django.contrib.auth import authenticate, login
from django.contrib.auth.hashers import check_password
from django.contrib import messages
from django.core.mail import send_mail
from django.contrib.auth import logout
from django.http import HttpResponseForbidden
from .models import *
from rest_framework import generics, status, permissions, viewsets
from .serializers import *
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework.permissions import AllowAny
from django.shortcuts import get_object_or_404
from dal import autocomplete
from rest_framework_simplejwt.views import TokenObtainPairView
from unibook.recommender.recommender_system import RecommenderSystem
from rest_framework.decorators import action
import datetime
from .permissions import *

recommender = RecommenderSystem()

class MyTokenObtainPairView(TokenObtainPairView):
    permission_classes = [AllowAny]
    """View to login a user."""

    authentication_classes = ()
    serializer_class = MyTokenObtainPairSerializer

class LogoutAndBlackListTokenView(APIView):
    authentication_classes = ()
    permission_classes = [AllowAny]

    def post(self, request):
        try:
            refresh_token = request.data["refresh_token"]
            token = RefreshToken(refresh_token)
            token.blacklist()
            return Response(status=status.HTTP_205_RESET_CONTENT)
        except Exception as e:
            return Response(status=status.HTTP_400_BAD_REQUEST)

class SignUpView(APIView):
    authentication_classes = ()
    permission_classes = [AllowAny]

    def post(self, request):
        sign_up_serializer = SignUpSerializer(data=request.data)
        if sign_up_serializer.is_valid():
            newuser = sign_up_serializer.save()
            if newuser:
                return Response(status=status.HTTP_201_CREATED)
        return Response(sign_up_serializer.errors, status=status.HTTP_400_BAD_REQUEST)



#User Views

class EditUser(generics.UpdateAPIView):
    queryset = User.objects.all()
    serializer_class = UpdateUserSerializer
    lookup_field = 'username'

class UserDetail(generics.RetrieveAPIView):
    serializer_class = UserSerializer
    queryset = User.objects.all()
    lookup_field = 'username'

class UserInfoView(APIView):
    serializer_class = UserSerializer

    def get(request):
        return Response(UserSerializer(request.user), status=status.HTTP_200_OK)

class CurrentUserView(APIView):
    def get(self, request):
        serializer = UserSerializer(request.user)
        return Response(serializer.data)

class UserList(generics.ListAPIView):
    serializer_class = UserSerializer
    queryset = User.objects.all()

class ChangePasswordView(generics.UpdateAPIView):
    """View to allow user to change their password."""

    serializer_class = ChangePasswordSerializer
    model = User

    def get_object(self, queryset=None):
        obj = self.request.user
        return obj

    def update(self, request, *args, **kwargs):
        self.object = self.get_object()
        serializer = self.get_serializer(data=request.data)

        if serializer.is_valid():
            # Check old password
            if not self.object.check_password(serializer.data.get("old_password")):
                return Response({"old_password": ["Wrong password."]}, status=status.HTTP_400_BAD_REQUEST)
            # set_password also hashes the password that the user will get
            self.object.set_password(serializer.data.get("new_password"))
            self.object.save()
            response = {
                'status': 'success',
                'code': status.HTTP_200_OK,
                'message': 'Password updated successfully',
                'data': []
            }

            return Response(response)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)



#Club Views

class CreateClub(generics.CreateAPIView):
    serializer_class = ClubSerializer
    queryset = Club.objects.all()


    def perform_create(self, serializer):
        """Create the chat room for the club when a club is created."""

        super().perform_create(serializer)
        club = get_club(serializer.data['id'])
        ChatRoom.objects.create(name=club.name, club_id=club.id, created_by_id = self.request.user.id)

class ClubDetail(generics.RetrieveAPIView):
    serializer_class = ClubSerializer
    lookup_field = 'club_id'

    def get_object(self, queryset=None, **kwargs):
        item = self.kwargs.get('club_id')
        return get_object_or_404(Club, id=item)

class EditClub(generics.UpdateAPIView):
    serializer_class = ClubSerializer
    queryset = Club.objects.all()
    lookup_field = 'club_id'

    def put(self, request, club_id):
        club = Club.objects.get(id=club_id)
        owner = User_Auth.objects.filter(club=club).get(rank='owner').user
        if(request.user == owner):
            edit_club_serializer = ClubSerializer(instance=club, data=request.data)
            if edit_club_serializer.is_valid():
                edit_club_serializer.save()
                return Response(status=status.HTTP_204_NO_CONTENT)
            else:
                return Response(status=status.HTTP_400_BAD_REQUEST)
        else:
            return Response(status=status.HTTP_400_BAD_REQUEST)

class ClubList(generics.ListAPIView):
    serializer_class = ClubSerializer

    def get_queryset(self):
        auths = User_Auth.objects.filter(user=self.request.user.pk)
        joined_clubs = []
        for x in range(len(auths)):
            joined_clubs.append(auths[x].club)
        #Returns list of all clubs user is not a part of/has applied to
        return list(set(Club.objects.all()) - set(joined_clubs))

class MyClubList(generics.ListAPIView):
    serializer_class = ClubSerializer

    def get_queryset(self):
        auths = User_Auth.objects.filter(user=self.request.user.pk)
        joined_clubs = []
        for x in range(len(auths)):
            joined_clubs.append(auths[x].club)
        return list(joined_clubs)

class ApplicantList(generics.ListAPIView):
    serializer_class = UserAuthSerializer
    lookup_field = 'club_id'

    def get_queryset(self):
        return User_Auth.objects.filter(club__id=self.kwargs.get('club_id'), rank='applicant')

class MemberList(generics.ListAPIView):
    serializer_class = UserAuthSerializer
    lookup_field = 'club_id'

    def get_queryset(self):
        return User_Auth.objects.filter(club__id=self.kwargs.get('club_id'), rank='member')

class OwnerList(generics.ListAPIView):
    serializer_class = UserAuthSerializer
    lookup_field = 'club_id'

    def get_queryset(self):
        return User_Auth.objects.filter(club__id=self.kwargs.get('club_id'), rank='owner')

class DeleteClub(generics.RetrieveDestroyAPIView):
    serializer_class = ClubSerializer
    queryset = Club.objects.all()
    lookup_field = 'club_id'

    def delete(self, request, club_id):
        club = Club.objects.get(id=club_id)
        owner = User_Auth.objects.filter(club=club).get(rank='owner').user
        if(request.user == owner):
            club.delete()
            return Response(status=status.HTTP_200_OK)
        else:
            return Response(status=status.HTTP_400_BAD_REQUEST)



#User_Auth Views

class CreateUserAuth(generics.CreateAPIView):
    serializer_class = UserAuthSerializer
    queryset = User_Auth.objects.all()

class UpdateUserAuth(generics.UpdateAPIView):
    serializer_class = UserAuthSerializer
    queryset = User_Auth.objects.all()

class getOwner(generics.RetrieveAPIView):
    serializer_class = UserAuthSerializer
    lookup_field = 'club_id'

    def get_queryset(self):
        return User_Auth.objects.filter(club__id=self.kwargs.get('club_id'),rank='owner')

class AcceptApplication(generics.UpdateAPIView):
    serializer_class = UserAuthSerializer
    queryset = User_Auth.objects.all()
    lookup_field = 'auth_id'

    def put(self, request, auth_id):
        auth = User_Auth.objects.get(id=auth_id)
        owner = User_Auth.objects.filter(club=auth.club).get(rank='owner').user
        if (request.user == owner):
            accept_applicant_serializer = UserAuthSerializer(instance=auth, data={'rank':'member'}, partial=True)
            if accept_applicant_serializer.is_valid():
                accept_applicant_serializer.save()
                return Response(status=status.HTTP_204_NO_CONTENT)
            else:
                return Response(status=status.HTTP_400_BAD_REQUEST)
        return Response(status=status.HTTP_400_BAD_REQUEST)

class RemoveUserFromClub(generics.RetrieveDestroyAPIView):
    serializer_class = UserAuthSerializer
    lookup_field = 'auth_id'

    def delete(self, request, auth_id):
        auth = User_Auth.objects.get(id=auth_id)
        owner = User_Auth.objects.filter(club=auth.club).get(rank='owner').user
        if(auth.user == owner):
            return Response(status=status.HTTP_400_BAD_REQUEST)
        if(request.user == owner and request.user!=auth.user):
            auth.delete()
            return Response(status=status.HTTP_200_OK)
        else:
            return Response(status=status.HTTP_400_BAD_REQUEST)

class UserAuthDetail(generics.RetrieveAPIView):
    serializer_class = UserAuthSerializer
    lookup_field = 'club_id'

    def get_queryset(self):
        return User_Auth.objects.filter(club__id=self.kwargs.get('club_id'), user__id=self.request.user.id)

class LeaveClubView(generics.RetrieveDestroyAPIView):
    """View to leave a club if user is member."""

    def delete(self, request, club_id):
        """Delete the user from the club if the user is a member in the club."""

        club = get_club(club_id)
        current_user = request.user
        try:
            auth = User_Auth.objects.filter(club=club).get(user=current_user).rank
            current_user_auth = User_Auth.objects.filter(club=club).get(user=request.user).rank
            if current_user_auth == 'owner':
                return Response(status=status.HTTP_400_BAD_REQUEST)
            if auth=='owner' or auth=='member':
                remove_member_from_club(current_user, club)
                return Response(status=status.HTTP_200_OK)
        except ObjectDoesNotExist:
            return Response(status=status.HTTP_400_BAD_REQUEST)
        else:
            return Response(status=status.HTTP_400_BAD_REQUEST)

class DeleteUserAuth(generics.RetrieveDestroyAPIView):
    serializer_class = UserAuthSerializer
    queryset = User_Auth.objects.all()



#Post Views

class CreatePostView(generics.CreateAPIView):

    def post(self, request, *args, **kwargs):
        #Get relation between club to post to and user attempting to post
        try:
            user_auth = User_Auth.objects.filter(club=self.kwargs.get('club_id')).get(user=request.user.pk)
        except User_Auth.DoesNotExist:
            return Response(status=status.HTTP_400_BAD_REQUEST)
        #Proceed if user is a member or owner of club they are trying to post in
        if(user_auth.club.id == self.kwargs.get('club_id') and user_auth.rank!='applicant'):
            create_post_serializer = PostSerializer(data=request.data)
            if create_post_serializer.is_valid():
                newpost = create_post_serializer.save()
                return Response(status=status.HTTP_201_CREATED)
        return Response(status=status.HTTP_400_BAD_REQUEST)

class EditPostView(generics.UpdateAPIView):
    lookup_field='post_id'

    def put(self, request, post_id):
        post = Post.objects.get(id=post_id)
        #Only allow user to edit post if they are author of post
        if(request.user == post.author):
            #Update retrieved post object if new data is valid
            edit_post_serializer = PostSerializer(instance=post, data=request.data)
            if edit_post_serializer.is_valid():
                edit_post_serializer.save()
                return Response(status=status.HTTP_204_NO_CONTENT)
        else:
            return Response(status=status.HTTP_400_BAD_REQUEST)

class DeletePostView(generics.RetrieveDestroyAPIView):

    def delete(self, request, post_id):
        post = Post.objects.get(id=post_id)
        #Only allow user to delete post if they are author of post
        if(request.user == post.author):
            post.delete()
            return Response(status=status.HTTP_200_OK)
        else:
            return Response(status=status.HTTP_400_BAD_REQUEST)

class ListClubPostsView(generics.ListAPIView):
    serializer_class = PostSerializer

    def get_queryset(self):
        return Post.objects.filter(club__id=self.kwargs.get('club_id'))



#Meeting Views

class CreateMeetingView(generics.CreateAPIView):
    lookup_field = 'club_id'
    serializer_class = MeetingSerializer

    def post(self, request, club_id):
        #Get relation between user attempting to create meeting and club they are creating meeting in
        try:
            user_auth = User_Auth.objects.filter(club=self.kwargs.get('club_id')).get(user=request.user.pk)
        except User_Auth.DoesNotExist:
            return Response(status=status.HTTP_400_BAD_REQUEST)
        #Only allow them to create a meeting for the club if they are a member or owner
        if(user_auth.club.id == self.kwargs.get('club_id') and user_auth.rank!='applicant'):
            create_meeting_serializer = MeetingSerializer(data=request.data)
            if create_meeting_serializer.is_valid():
                newmeeting = create_meeting_serializer.save()

                subject = "You've been added toa  meeting"
                message = 'To view the meeting click here: ...'
                recipient_list = User_Auth.objects.filter(club=self.kwargs.get('club_id')).values_list('user__email', flat=True)
                send_mail(
                    subject,
                    message,
                    'https://limitless-depths-09294.herokuapp.com/',
                    recipient_list
                )

                return Response(status=status.HTTP_201_CREATED)

        return Response(status=status.HTTP_400_BAD_REQUEST)

class ClubMeetingDetail(generics.RetrieveAPIView):
    """View to see the meeting's detail in the club."""
    serializer_class = MeetingSerializer
    queryset = Meeting.objects.all()
    lookup_field = 'club_id'


class MeetingListView(generics.ListAPIView):
    """View to see all meetings created in the club."""

    serializer_class = MeetingSerializer
    lookup_field = 'club_id'

    def get_queryset(self):
        club = get_club(self.kwargs.get('club_id'))
        meetings = get_meetings(club)
        return meetings

class EditMeetingView(generics.UpdateAPIView):
    queryset = Meeting.objects.all()
    serializer_class = UpdateMeetingSerializer
    lookup_field = 'id'


class ShowEditMeeting(generics.RetrieveAPIView):
    serializer_class = UpdateMeetingSerializer
    queryset = Meeting.objects.all()
    lookup_field = 'id'

class DeleteMeetingView(generics.RetrieveDestroyAPIView):
    lookup_field = 'meeting_id'

    def delete(self, request, meeting_id):
        meeting = Meeting.objects.get(id=meeting_id)
        user = self.request.user
        club = meeting.club
        owner = User_Auth.objects.filter(club=club).get(rank='owner').user
        #Only allow user to delete meeting if they created it or are club owner
        if(user==meeting.creator or user==owner):
            meeting.delete()

            subject = "One of youe meetings has been deleted  meeting"
            message = 'Please log in and check which meeting has been cancelled'
            recipient_list = User_Auth.objects.filter(club=self.kwargs.get('club_id')).values_list('user__email', flat=True)
            send_mail(
                subject,
                message,
                'https://limitless-depths-09294.herokuapp.com/',
                recipient_list
                )

            return Response(status=status.HTTP_200_OK)
        else:
            return Response(status=status.HTTP_400_BAD_REQUEST)



#Chat Room Views

class ChatRoomViewSet(viewsets.ModelViewSet):
    model = ChatRoom
    serializer_class = ChatRoomSerializer
    queryset = ChatRoom.objects.all()


    @action(methods=['delete'], detail=True, url_path='remove-user/(?P<user_id>[^/.]+)')
    def remove_user(self, request, pk, user_id):
        obj = self.get_object()
        obj.members.remove(user_id)
        return Response(status=200)

    @action(methods=['post'], detail=True, url_path='add-user/(?P<user_id>[^/.]+)')
    def add_user(self, request, pk, user_id):
        obj = self.get_object()
        obj.members.add(user_id)
        return Response(status=200)


    def get_queryset(self):
        # GET /api/chat-rooms/?club_id=123

        queryset = self.queryset.filter(club_id=self.request.GET.get('club_id'))

        queryset  = queryset.filter(members=self.request.user) # only show me chats where I am a member

        #add more filters if needed

        return queryset



#Message Views

class MessageViewSet(viewsets.ModelViewSet):
    model = Message
    serializer_class = MessageSerializer
    queryset = Message.objects.all()

    def get_queryset(self):

        # GET /api/messages/?chat_room_id=123
        return self.queryset.filter(chat_room=self.request.GET.get('club_id'))

    def post(self, request):
        model = Message
        serializer_class = MessageSerializer
        request.data.created_by = request.user
        message = serializer_class(instance=model,data=request.data)

        if message.is_valid():
            message.save()
        return  Message.objects.add(message)



#Book Views

class ListBooks(generics.ListAPIView):
    serializer_class = BookSerializer

    def get_queryset(self):
        return Book.objects.all()[:8000]

class GetBooksToShow(APIView):

    def get(self,request):
        user = self.request.user
        books_to_show = get_books_to_show(user.id)

        return Response(data={"books_to_show":books_to_show}, status=status.HTTP_200_OK)

class CreateBookRatings(generics.CreateAPIView):
    serializer_class = BookRatingSerializer

    def post(self, request):
        current_user = self.request.user
        book_rating_serializer = BookRatingSerializer(data=request.data)
        books_to_show = get_books_to_show(current_user.id)
        if book_rating_serializer.is_valid():
            book_isbn = book_rating_serializer.data.get("book")
            book = Book.objects.get(isbn=book_isbn)
            added_book = add_to_book_rating_csv(book, book_rating_serializer.data.get("rating"), current_user.id)
            if (added_book == None):
                messages.add_message(request, messages.ERROR, f"Already rated {book_rating_serializer.data.get('book').title}")
                return Response(data={"books_to_show":books_to_show}, status=status.HTTP_400_BAD_REQUEST)
            return Response(data={"books_to_show":books_to_show}, status=status.HTTP_200_OK)

        else:
            return Response(data={"books_to_show":books_to_show}, status=status.HTTP_400_BAD_REQUEST)



#Recommender Views

class UserRecommenderView(APIView):
    serializer_class = BookSerializer

    def get(self, request):
        books_isbn = recommender.get_recommendations_for_user(request.user.id)
        book_recommendations = get_books_from_isbn(books_isbn)
        serializer = BookSerializer(book_recommendations, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

class ClubRecommenderView(generics.ListAPIView):
    serializer_class = BookSerializer

    def get_queryset(self, *args, **kwargs):
        club = get_club(self.kwargs.get('club_id'))
        owner = list(get_owners(club))
        members = list(get_members(club))
        club_users = members + owner
        user_id = list(map(lambda user: user.id, club_users))
        books_isbn = recommender.get_recommendations_for_club(user_id)
        book_recommendations = get_books_from_isbn(books_isbn)
        return book_recommendations
