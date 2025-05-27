from surprise import AlgoBase
from surprise import PredictionImpossible
from .book_data import BookData
import math
import numpy as np
import heapq

class ContentBasedAlgorithm(AlgoBase):
    """Content based algorithm to be used for the recommender."""

    def __init__(self, k=40, sim_options={}):
        """Load and initialise the book data."""

        AlgoBase.__init__(self)
        books = BookData()

        self.years = books.get_years()
        self.authors = books.get_authors()
        self.publishers = books.get_publishers()
        self.k = k

    def fit(self, trainset):
        AlgoBase.fit(self, trainset)

        # Compute item similarity matrix based on content attributes

        print("Computing content-based similarity matrix...")

        # Compute distance for every book combination as a 2x2 matrix
        self.similarities = np.zeros((self.trainset.n_items, self.trainset.n_items))

        for this_rating in range(self.trainset.n_items):
            if (this_rating % 100 == 0):
                print(this_rating, " of ", self.trainset.n_items)
            for other_rating in range(this_rating+1, self.trainset.n_items):
                this_book_id = self.trainset.to_raw_iid(this_rating)
                other_book_id = self.trainset.to_raw_iid(other_rating)
                year_similarity = self.compute_year_similarity(this_book_id, other_book_id, self.years)
                # author_similarity = self.compute_author_similarity(this_book_id, other_book_id, self.authors)
                # publisher_similarity = self.compute_publisher_similarity(this_book_id, other_book_id, self.publishers)
                self.similarities[this_rating, other_rating] = year_similarity
                # self.similarities[this_rating, other_rating] = author_similarity
                # self.similarities[this_rating, other_rating] = publisher_similarity
                # self.similarities[this_rating, other_rating] = year_similarity * author_similarity
                # self.similarities[this_rating, other_rating] = year_similarity * publisher_similarity
                # self.similarities[this_rating, other_rating] = author_similarity * publishers_similarity
                # self.similarities[this_rating, other_rating] = author_similarity * year_similarity *  publisher_similarity
                self.similarities[other_rating, this_rating] = self.similarities[this_rating, other_rating]

        print("...done.")

        return self

    def compute_year_similarity(self, book1, book2, years):
        """Compute the year similarity between two books."""

        diff = abs(years[book1] - years[book2])
        sim = math.exp(-diff / 10.0)
        return sim

    def compute_author_similarity(self, book1, book2, authors):
        """Compute the author similarity between two books."""

        author1 = authors[book1]
        author2 = authors[book2]
        if author1 == author2:
            return 1
        return 0

    def compute_publisher_similarity(self, book1, book2, publishers):
        """Compute the publisher similarity between two books."""

        publisher1 = publishers[book1]
        publisher2 = publishers[book2]
        if publisher1 == publisher2:
            return 1
        return 0

    def estimate(self, user, item):
        """Estimate a predicted rating."""

        if not (self.trainset.knows_user(user) and self.trainset.knows_item(item)):
            raise PredictionImpossible('User and/or item is unkown.')

        # Build up similarity scores between this item and everything the user rated
        neighbours = []
        for rating in self.trainset.ur[user]:
            similarity = self.similarities[item,rating[0]]
            neighbours.append( (similarity, rating[1]) )

        # Extract the top-K most-similar ratings
        k_neighbours = heapq.nlargest(self.k, neighbours, key=lambda t: t[0])

        # Compute average sim score of K neighbours weighted by user ratings
        sim_total = weighted_sum = 0
        for (sim_score, rating) in k_neighbours:
            if (sim_score > 0):
                sim_total += sim_score
                weighted_sum += sim_score * rating

        if (sim_total == 0):
            raise PredictionImpossible('No neighbours')

        predicted_rating = weighted_sum / sim_total

        return predicted_rating
