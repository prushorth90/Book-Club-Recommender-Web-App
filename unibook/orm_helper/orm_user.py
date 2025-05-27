"""Helper functions for users."""
from django.core.exceptions import ObjectDoesNotExist
from unibook.models import User_Auth, User

def is_owner(user, user_club):
    """Verify if the user is an owner in the club."""

    if get_authorization(user, user_club) == 'owner':
        return True
    return False

def is_member(user, user_club):
    """Verify if the user is a member in the club."""

    if get_authorization(user, user_club) == 'member':
        return True
    return False

def is_applicant(user, user_club):
    """Verify if the user is an applicant in the club."""

    if get_authorization(user, user_club) == 'applicant':
        return True
    return False

def get_user(user_id):
    """Get the user object from the database."""

    try:
        user = User.objects.get(id=user_id)
    except ObjectDoesNotExist:
        return None
    return user

def get_owners(club):
    """Get the owner in the given club."""

    owners = (User_Auth.objects
                        .filter(club=club)
                        .filter(rank="owner")
                        .values_list('user__id', flat=True))
    return User.objects.filter(id__in=owners)

def get_applicants(club):
    """Get all the applicants in the given club."""

    applicants = (User_Auth.objects
                        .filter(club=club)
                        .filter(rank="applicant")
                        .values_list('user__id', flat=True))
    return User.objects.filter(id__in=applicants)

def get_members(club):
    """Get all the members in the given club."""

    members = (User_Auth.objects
                        .filter(club=club)
                        .filter(rank="member")
                        .values_list('user__id', flat=True))
    return User.objects.filter(id__in=members)

def get_authorization(user, user_club):
    """Get the authorization of current user in the club."""

    if user is None or user.is_anonymous:
        return ""
    try:
        user = User.objects.get(id = user_club.id)
        auth = User_Auth.objects.filter(club=user_club).get(user=user).rank
    except ObjectDoesNotExist:
        return None

    return auth

def set_auth(user, club, auth):
    """Set the authorization of the user in the club."""

    try:
        (User_Auth.objects
            .filter(user=user)
            .filter(club=club)
            .update(rank=auth))
    except ObjectDoesNotExist:
        messages.add_message(request, messages.ERROR, "Did not success update")
