from rest_framework import permissions
from unibook.orm_helper.orm_user import get_authorization
from unibook.orm_helper.orm_club import get_club

class LoginProhibitedPermission(permissions.BasePermission):
    """Permission to not allow user to access a view if user is logged in."""

    def has_permission(self, request, view):
        """The user will not have permission if user is authenticated."""

        return not request.user.is_authenticated

class ApplicantsOnlyPermission(permissions.BasePermission):
    """Permission to not allow user to access a view if user is not an applicant in the club."""

    message = 'You need to be an applicant of the club.'

    def has_permission(self, request, view):
        """The user will not have permission if the user is not an applicant in the club."""

        club = get_club(view.kwargs.get('club_id'))
        return get_authorization(request.user, club) == 'applicant'

class MembersOnlyPermission(permissions.BasePermission):
    """Permission to not allow user to access a view if user is an applicant in the club."""

    message = 'You need to be a member of the club.'

    def has_permission(self, request, view):
        """The user will not have permission if the user is an applicant in the club."""

        club = get_club(view.kwargs.get('club_id'))
        authorization = get_authorization(request.user, club)
        return not (authorization == None or authorization == 'applicant')

class OwnerOnlyPermission(permissions.BasePermission):
    """Permission to not allow user to access a view if user is not an owner in the club."""

    message = 'You must be an owner.'

    def has_permission(self, request, view):
        """The user will not have permission if the user is an applicant in the club."""

        club = get_club(view.kwargs.get('club_id'))
        return get_authorization(request.user, club) == 'owner'