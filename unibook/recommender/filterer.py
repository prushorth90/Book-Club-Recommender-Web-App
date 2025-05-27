import pandas as pd
import datetime

class BookFilterer:
    """Book filterer where it filters all invalid data in the csv files."""

    ratings_path = 'recommender/book_dataset/BX_Book_Ratings.csv'
    books_path = 'recommender/book_dataset/BX_Books.csv'

    def filter_books(self):
        """Filter all the invalid data in books."""

        books = pd.read_csv(self.books_path, sep=';', encoding='ISO-8859-1')

        #remove zero years e.g Book Abc: Year published: 0
        books_without_zero_year = books[books['Year-Of-Publication'] != 0]

        #remove books with year of publication greater than the current year
        current_year = datetime.datetime.now().year
        books_less_than_current_year = books_without_zero_year[books_without_zero_year['Year-Of-Publication'] < current_year]

        #remove  url-s and url-l keep url-m
        books_less_than_current_year.drop(['Image-URL-S','Image-URL-L'], axis=1, inplace=True)
        books_less_than_current_year.to_csv(self.books_path, sep=';',encoding='ISO-8859-1', index=False)

    def filter_book_ratings(self):
        """Filter all the invalid data in ratings."""

        ratings = pd.read_csv(self.ratings_path, sep=';', encoding='ISO-8859-1')
        ratings_without_zero = self.filter_zero_ratings(ratings)
        ratings_without_invalid_book = self.filter_invalid_books(ratings_without_zero)
        ratings_with_filtered_users = self.filter_users_rated_less_than_k_books(15, ratings_without_invalid_book)
        ratings_with_filtered_books = self.filter_books_rated_less_than_k_times(10, ratings_with_filtered_users)
        ratings_with_filtered_books.to_csv(self.ratings_path, sep=';',encoding='ISO-8859-1', index=False)

    def filter_zero_ratings(self, ratings):
        """Remove book ratings which are rated zero."""

        ratings_without_zero = ratings[ratings['Book-Rating'] != 0]
        return ratings_without_zero

    def filter_invalid_books(self, ratings):
        """Filter book ratings with invalid isbn."""

        books = pd.read_csv(self.books_path, sep=';', encoding='ISO-8859-1')
        isbn = books['ISBN'].to_list()
        ratings_without_invalid_book = ratings[ratings['ISBN'].isin(isbn)]
        return ratings_without_invalid_book

    def filter_users_rated_less_than_k_books(self, minimum_books_required, ratings):
        """Filter out users that rated less than the minimum number of times a user must rate a book to have better rmse."""

        num_books_user_rated = ratings['User-ID'].value_counts()
        users = num_books_user_rated[num_books_user_rated >= minimum_books_required].index.to_list()
        filtered_ratings = ratings[ratings['User-ID'].isin(users)]
        return filtered_ratings

    def filter_books_rated_less_than_k_times(self, minimum_times_rated, ratings):
        """Filter out books that have been rated less than the minimum times it needs to be rated to have better rmse."""

        num_of_times_rated = user_match['ISBN'].value_counts()
        books = num_of_times_rated[num_of_times_rated >= minimum_times_rated].index.to_list()
        filtered_ratings = ratings[ratings['ISBN'].isin(books)]
        return filtered_ratings
