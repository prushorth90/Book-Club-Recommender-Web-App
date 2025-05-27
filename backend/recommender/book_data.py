import csv
import pandas as pd

from surprise import Dataset
from surprise import Reader
import numpy as np

from collections import defaultdict

class BookData:
    """Book data class to get all the details."""

    isbn_to_title = {}
    title_to_isbn = {}
    ratings_path = 'unibook/recommender/book_dataset/BX_Book_Ratings.csv'
    books_path = 'unibook/recommender/book_dataset/BX_Books.csv'

    def load_book_data(self):
        """ Load the dataset for book ratings and books """

        ratings_dataset = 0
        self.isbn_to_title  = {}
        self.title_to_isbn  = {}

        reader = Reader(line_format='user item rating', sep=';', rating_scale=(1,10), skip_lines=1)

        ratings_dataset = Dataset.load_from_file(self.ratings_path, reader=reader)

        with open(self.books_path, newline='', encoding='ISO-8859-1') as csvfile:
                book_reader = csv.reader(csvfile, delimiter=';')
                next(book_reader)  #Skip header line
                for row in book_reader:
                    isbn = row[0]
                    title = row[1]
                    self.isbn_to_title[isbn] = title
                    self.title_to_isbn[title] = isbn

        return ratings_dataset

    def get_user_ratings(self, user):
        """ Get the user ratings """

        user_ratings = []
        hit_user = False
        with open(self.ratings_path, newline='') as csvfile:
            rating_reader = csv.reader(csvfile, delimiter=';')
            next(rating_reader)
            for row in rating_reader:
                user_id = int(row[0])
                if (user == user_id):
                    isbn = row[1]
                    rating = float(row[2])
                    user_ratings.append((isbn, rating))
                    hit_user = True
                if (hit_user and (user != user_id)):
                    break

        return user_ratings

    def create_imaginary_user(self, members_in_club):
        """Create an imaginary user with combined ratings to represent a club and add it to csvfile."""

        df_ratings = pd.read_csv(self.ratings_path, sep=';', encoding='ISO-8859-1')
        df_members_in_club = df_ratings[df_ratings['User-ID'].isin(members_in_club)]
        df_members_in_club = round(df_members_in_club.groupby('ISBN').mean()).reset_index()
        df_members_in_club = df_members_in_club.reindex(columns=["User-ID","ISBN", "Book-Rating"])
        df_members_in_club['Book-Rating'] = df_members_in_club['Book-Rating'].astype(np.int64)
        club_rep = df_ratings['User-ID'].max() + 1
        df_members_in_club['User-ID'] = club_rep
        df_members_in_club.to_csv(self.ratings_path, mode='a', header=False, index=False, sep=';')
        return club_rep

    def delete_imaginary_club_rep(self, club_rep):
        """Delete imaginary user that represents a club."""

        df_ratings = pd.read_csv(self.ratings_path, sep=';', encoding='ISO-8859-1')
        df_ratings.drop(df_ratings.index[df_ratings['User-ID'] == club_rep], inplace=True)
        df_ratings.to_csv(self.ratings_path,index=False, sep=';')

    def get_popularity_ranks(self):
        """ Get the popularity rankings for the book """

        ratings = defaultdict(int)
        rankings = defaultdict(int)
        with open(self.ratings_path, newline='') as csvfile:
            rating_reader = csv.reader(csvfile, delimiter=';')
            next(rating_reader)
            for row in rating_reader:
                isbn = row[1]
                ratings[isbn] += 1
        rank = 1
        for isbn, rating_count in sorted(ratings.items(), key=lambda x: x[1], reverse=True):
            rankings[isbn] = rank
            rank += 1
        return rankings

    def get_authors(self):
        """ Get the authors of the book"""

        authors = defaultdict(list)
        with open(self.books_path, newline='', encoding='ISO-8859-1') as csvfile:
            book_reader = csv.reader(csvfile, delimiter=';')
            next(book_reader)  #Skip header line
            for row in book_reader:
                isbn = row[0]
                author = row[2]
                authors[isbn] = author
        return authors

    def get_publishers(self):
        """ Get the book publisher """

        publishers = defaultdict(list)
        with open(self.books_path, newline='', encoding='ISO-8859-1') as csvfile:
            book_reader = csv.reader(csvfile, delimiter=';')
            next(book_reader)  #Skip header line
            for row in book_reader:
                isbn = row[0]
                publisher = row[4]
                publishers[isbn] = publisher
        return publishers

    def get_years(self):
        """ Get the year book is made """

        years = defaultdict(int)
        with open(self.books_path, newline='', encoding='ISO-8859-1') as csvfile:
            book_reader = csv.reader(csvfile, delimiter=';')
            next(book_reader)
            for row in book_reader:
                isbn = row[0]
                year = row[3]
                years[isbn] = int(year) # Add a try/catch
        return years

    def get_book_title(self, isbn):
        """ Get the book title """

        if isbn in self.isbn_to_title:
            return self.isbn_to_title[isbn]
        else:
            return ""

    def get_book_isbn(self, bookTitle):
        """ Get the book ISBN """

        if bookTitle in self.title_to_isbn:
            return self.title_to_isbn[bookTitle]
        else:
            return ""

    def get_image_m_url(self):
        """ Get image url for medium size"""

        urls = defaultdict(list)
        with open(self.books_path, newline='', encoding='ISO-8859-1') as csvfile:
            book_reader = csv.reader(csvfile, delimiter=';')
            next(book_reader)  #Skip header line
            for row in book_reader:
                isbn = row[0]
                url = row[6]
                urls[isbn] = url
        return urls
