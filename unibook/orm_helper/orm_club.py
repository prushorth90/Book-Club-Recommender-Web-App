from unibook.models import User_Auth,Club, Meeting
from django.core.exceptions import ObjectDoesNotExist
from .orm_user import *

def is_user_in_club(user, club):
    """Check if a given user is in the club."""

    try:
        user_auth = User_Auth.objects.get(user=user, club=club)
    except ObjectDoesNotExist:
        return False
    return True

def get_club(club_id):
    """Get the club object from the club id."""

    try:
        club = Club.objects.get(id=club_id)
    except ObjectDoesNotExist:
        return None
    return club

def get_current_user_clubs(user):
    """Get the clubs the user is in."""

    try:
        # User may have more than one club
        current_user_clubs_id = User_Auth.objects.filter(user=user).values_list('club__id', flat=True)
        current_user_clubs = Club.objects.filter(id__in=current_user_clubs_id)
    except ObjectDoesNotExist:
        return None
    return current_user_clubs

def get_count_of_users_in_club(user_club):
    """Get the count of users in a club."""

    count = User_Auth.objects.filter(club=user_club).values_list('user__id', flat=True).count()
    return count

def get_count_of_user_auth_in_club(club, auth):
    """Get the number of users in club with the respective authorization."""

    count = User_Auth.objects.filter(club=club).filter(rank=auth).values_list('user__id', flat=True).count()
    return count

def remove_clubs(current_user):
    """Remove clubs the given user is in."""

    user_clubs = get_current_user_clubs(current_user)
    for club in user_clubs:
        # 1. In club table, delete if there is only a single user
        count_all_users_in_club = get_count_of_users_in_club(club)
        if count_all_users_in_club == 1:
            club.delete()
            continue
        # 2. In club table, delete where only applicants and owner
        if is_owner(current_user, club):
            count_applicants_in_club = get_count_of_user_auth_in_club(club, 'applicant')
            if count_applicants_in_club + 1 == count_all_users_in_club:
                # may need to update applicants
                club.delete()
            else:
                # 3. >=1 member in addition to applicants and owner
                # Must transfer ownership to a member
                return (False, club.id)

    return (True,0)

def get_other_clubs(user):
    """Get all other clubs the user is not in."""

    try:
        my_clubs = get_current_user_clubs(user)
        other_clubs = Club.objects.exclude(id__in=my_clubs)
    except ObjectDoesNotExist:
        return None
    return other_clubs

def get_meetings(club):
    """Get all the meetings created in the club."""

    return Meeting.objects.filter(club=club)

def get_meeting_in_club(meeting_id):
    """Get the meeting object in the club."""

    try:
        meeting = Meeting.objects.get(id=meeting_id)
    except ObjectDoesNotExist:
        return None
    return meeting

def remove_member_from_club(user, club):
    """Remove a member from the club."""

    try:
        User_Auth.objects.get(user=user, club=club).delete()
    except ObjectDoesNotExist:
        return None
