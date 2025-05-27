from .surprise_recommender import Recommender, SimpleCollabRecommender
from .spark_recommender import SparkRecommender
from .book_data import BookData

class RecommenderSystem:
    """Main system for the recommender where user can choose which recommender to use.
        The system allows recommending books to a user or to a club."""

    def __init__(self):
        self.recommender = Recommender()
        trainset = self.recommender.build_and_get_trainset()
        self.recommender.create_model('SVD', 'cosine', True)
        self.recommender.train_model(trainset)

    def get_recommendations_for_club(self, members):
        """Get recommendations for a club"""

        book_data = BookData()
        club_as_user = book_data.create_imaginary_user(members)
        recommendations = self.recommender.get_recommendations(club_as_user)
        book_data.delete_imaginary_club_rep(club_as_user)
        return recommendations

    def get_recommendations_for_user(self, user_id):
        """Get recommendations for a user."""

        recommendations = self.recommender.get_recommendations(user_id)
        return recommendations

    def retrain_model(self):
        """Retrain the model with a new trainSet."""

        self.recommender.load_data_and_rankings()
        trainset = self.recommender.build_and_get_trainset()
        self.recommender.train_model(trainset)

    def print_recommendations(self, recommendations):
        """Print the recommendations for the user."""

        for isbn in recommendations:
            print(self.recommender.books.get_book_title(isbn))
