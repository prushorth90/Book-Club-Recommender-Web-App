"""Database Seeder"""
from unibook.orm_helper.orm_club import *
from unibook.orm_helper.orm_user import *
from unibook.models import Club, User, User_Auth
from django.core.management.base import BaseCommand
from django.db import IntegrityError
from faker import Faker
import random
import pandas as pd
from django.conf import settings

class Command(BaseCommand):
    """Database Seeder"""

    ratings_path = 'unibook/recommender/book_dataset/BX_Book_Ratings.csv'
    ratings = pd.read_csv(ratings_path, sep=';', encoding='ISO-8859-1')
    user_id_csv = ratings['User-ID'].unique().tolist()[:settings.NUM_USER_TO_SEED]

    def __init__(self):
        super().__init__()
        self.faker = Faker('en_GB', 0)
        self.authorisation_levels=['applicant', 'member', 'owner']
        self.user_counter = 0
        self.club_counter = 0
        self.club_owners = {}

    def seed_random_user(self):
        first_name = self.faker.first_name()
        last_name = self.faker.last_name()
        email = first_name + last_name + '@example.org'
        username = first_name + last_name
        while(User.objects.filter(username=username).exists()):
            username = f'{username}random.randint(0,100)'
            email = username+'@example.org'
        bio = self.faker.sentence()

        randomUser = User.objects.create_user(
            pk=self.user_id_csv[0],
            first_name=first_name,
            last_name=last_name,
            email=email,
            username=username,
            bio=bio,
            password='Password123',
        )
        self.user_id_csv.pop(0)

        self.user_counter+=1
        return randomUser

    def seed_random_club(self):
        name = self.faker.text(max_nb_chars=20)
        while(Club.objects.filter(name=name).exists()):
            name = self.faker.text(max_nb_chars=20)
        description = self.faker.sentence()
        members_capacity = random.randint(2, 50)

        randomClub = Club.objects.create(
            name=name,
            description=description,
            members_capacity=members_capacity
        )

        self.club_counter+=1
        return randomClub

    def handle(self, *args, **options):
        for i in range(0,settings.NUM_USER_TO_SEED):
            randomUser = self.seed_random_user()
        for i in range(0,5):
            randomClub = self.seed_random_club()
        for club in Club.objects.all():
            owner=User.objects.all()[random.randint(0,self.user_counter)]
            if not is_owner(owner, club):
                try:
                    User_Auth.objects.create(
                        rank='owner',
                        club=club,
                        user=owner
                    )
                except:
                    pass
            for i in range(0, random.randint(0,self.user_counter)):
                user = User.objects.all()[random.randint(0,self.user_counter)]
                if not is_owner(user, club) and not is_member(user,club):
                    try:
                        User_Auth.objects.create(
                            rank='member',
                            club=club,
                            user=user
                        )
                    except:
                        pass
            for i in range(0, random.randint(0,self.user_counter)):
                user = User.objects.all()[random.randint(0,self.user_counter)]
                if not is_owner(user, club) and not is_member(user,club) and not is_applicant(user,club):
                    try:
                        User_Auth.objects.create(
                            rank='applicant',
                            club=club,
                            user=user
                        )
                    except:
                        pass
