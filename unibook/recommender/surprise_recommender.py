from .book_data import BookData
from surprise import KNNBasic,KNNWithMeans,KNNWithZScore,KNNBaseline,SVD,SVDpp,NormalPredictor
from .algorithms import ContentBasedAlgorithm
import heapq
from collections import defaultdict
from operator import itemgetter
from .evaluation.dataset_evaluator import DatasetEvaluator
from .evaluation.recommender_metrics import RecommenderMetrics

class Recommender():
    """Recommender that uses the surprise library. It consists of different algorithms.
        The recommender includes both content based filtering and collaborative filtering."""

    algorithms = {
        'KNNBasic': KNNBasic(),
        'KNNWithMeans': KNNWithMeans(),
        'KNNWithZScore': KNNWithZScore(),
        'KNNBaseline': KNNBaseline(),
        'NormalPredictor': NormalPredictor(),
        'SVD': SVD(),
        'SVDpp': SVDpp(),
        'ContentBasedAlgorithm': ContentBasedAlgorithm()
    }

    def __init__(self):
        """Initialise the dataset."""

        self.books = BookData()
        self.load_data_and_rankings()

    def load_data_and_rankings(self):
        """Load the book data and rankings."""

        print("Loading book data...")
        self.data = self.books.load_book_data()
        self.rankings = self.books.get_popularity_ranks()

    def build_and_get_trainset(self):
        """Build the full trainset from the data."""

        self.trainset = self.data.build_full_trainset()
        return self.trainset

    def create_sim_options(self, sim_metric, is_user_based):
        """Create sim options - e.g cosine,msd,pearson,pearson baseline."""

        sim_options = {'name': sim_metric, 'user_based': is_user_based}
        return sim_options

    def create_model(self, algorithm, sim_metric=None, is_user_based=None):
        """Create the model to be fitted with options."""

        self.model = self.algorithms[algorithm]
        if (sim_metric != None and is_user_based != None):
            sim_options = self.create_sim_options(sim_metric, is_user_based)
            self.model.sim_options = sim_options
        return self.model

    def train_model(self, trainset):
        """Train the model with the trainset."""

        self.model.fit(trainset)

    def get_anti_testset_for_user(self, user_id):
        """Get the anti test set for user."""

        fill = self.trainset.global_mean
        anti_testset = []
        if not self.trainset.knows_user(user_id):
            # Load the data again to see if the data has been updated with new users
            self.load_data_and_rankings()
            self.build_and_get_trainset()

        user_inner_id = self.trainset.to_inner_uid(user_id)
        user_items = set([j for (j, _) in self.trainset.ur[user_inner_id]])
        anti_testset += [(self.trainset.to_raw_uid(user_inner_id), self.trainset.to_raw_iid(item), fill) for
                                 item in self.trainset.all_items() if
                                 item not in user_items]
        return anti_testset

    def get_recommendations(self, user_id, k=10):
        """ Get top k recommendations for a user """

        try:
            test = self.get_anti_testset_for_user(str(user_id))
        except:
            return ''
        predictions = self.model.test(test)
        recommendations = []

        for userid, book_id, actual_rating, estimated_rating, _ in predictions:
            recommendations.append((book_id, estimated_rating))

        recommendations.sort(key=lambda x: x[1], reverse=True)
        books_recommendations = [recommendation[0] for recommendation in recommendations][:k]

        return books_recommendations

class SimpleCollabRecommender(Recommender):
    """The recommender that consists of only simple item-based filtering and simple user-based filtering.
        Full evaluation is not possible."""

    def __init__(self):
        super().__init__()

    def build_sims_matrix(self):
        """Build sims matrix."""

        self.sims_matrix = self.model.compute_similarities()

    def train_model(self, trainset):
        """Train the model with the trainset and build sims matrix."""

        self.model.fit(trainset)
        self.build_sims_matrix()

    def get_user_ratings(self, user_inner_id):
        """Get the user ratings."""

        user_ratings = self.trainset.ur[user_inner_id]
        return user_ratings

    def get_similar_users(self, user_inner_id):
        """ Find similar users to current user """

        similarity_row = self.sims_matrix[user_inner_id]
        similar_users = []
        for inner_id, score in enumerate(similarity_row):
            if inner_id != user_inner_id:
                similar_users.append( (inner_id, score) )

        return similar_users

    def rank_candidates(self, k_neighbours):
        """Rank the available candidates weighted by user similarity or rating."""

        candidates = defaultdict(float)
        if (self.model.sim_options.get('user_based') == True):
            # User-based collaborative filtering
            # Get the stuff they rated, and add up ratings for each item (weighted by user similarity)
            for similar_user in k_neighbours:
                inner_id = similar_user[0]
                user_similarity_score = similar_user[1]
                their_ratings = self.trainset.ur[inner_id]
                for rating in their_ratings:
                    candidates[rating[0]] += (rating[1] / 10) * user_similarity_score
        else:
            # Item-based collaborative filtering
            # Get similar items to stuff user liked (weighted by rating)
            for item_id, rating in k_neighbours:
                similarity_row = self.sims_matrix[item_id]
                for inner_id, score in enumerate(similarity_row):
                    candidates[inner_id] += score * (rating / 10.0)

        return candidates

    def get_books_already_seen(self, user_inner_id):
        """ Get the books already seen by the current user"""

        seen = {}
        for item_id, rating in self.trainset.ur[user_inner_id]:
            seen[item_id] = 1
        return seen

    def get_recommendations(self, user_id, k=10):
        """ Get the recommendations for the user """

        user_id = str(user_id)
        if not self.trainset.knows_user(user_id):
            # Load the data again to see if the data has been updated with new users
            self.load_data_and_rankings()
            self.trainset = self.build_and_get_trainset()
            self.train_model(self.trainset)

        user_inner_id = self.trainset.to_inner_uid(user_id)

        if (self.model.sim_options.get('user_based') == True):
            iterable = self.get_similar_users(user_inner_id)
        else:
            iterable = self.get_user_ratings(user_inner_id)

        k_neighbours = heapq.nlargest(k, iterable, key=lambda t: t[1])
        candidates = self.rank_candidates(k_neighbours)
        seen = self.get_books_already_seen(user_inner_id)

        pos = 0
        recommendations = []
        for item_id, rating_sum in sorted(candidates.items(), key=itemgetter(1), reverse=True):
            if not item_id in seen:
                book_id = self.trainset.to_raw_iid(item_id)
                recommendations.append(book_id)
                pos += 1
                if (pos > k):
                    break

        return recommendations

    def evaluate(self, filter, sim_metrics, algorithms):
        """Evaluate the simple collborative filtering recommender system.
            It is not possible to evaluate the simple collborative filtering with rmse and mae."""

        if filter == 'user':
            user_based = True
        elif filter == 'item':
            user_based = False
        else:
            print("It is not possible to evaluate with this filter.")
            return

        eval_data = DatasetEvaluator(self.data, self.rankings)
        self.trainset = eval_data.get_LOOCV_trainset()

        for metric in sim_metrics:
            for algorithm in algorithms:

                model = self.create_model(algorithm, metric, user_based)
                self.train_model(self.trainset)
                self.build_sims_matrix()
                print(self.model)

                left_out_test_set = eval_data.get_LOOCV_testset()

                # Build up dict to lists of (int(bookID), predictedrating) pairs
                top_n = defaultdict(list)
                k = 10
                for uiid in range(self.trainset.n_users):
                    if (self.model.sim_options.get('user_based') == True):
                        iterable = self.get_similar_users(uiid)
                    else:
                        iterable = self.get_user_ratings(uiid)

                    k_neighbours = heapq.nlargest(k, iterable, key=lambda t: t[1])
                    candidates = self.rank_candidates(k_neighbours)
                    seen = self.get_books_already_seen(uiid)

                    # Get top-rated items from similar users:
                    pos = 0
                    for item_id, rating_sum in sorted(candidates.items(), key=itemgetter(1), reverse=True):
                        if not item_id in seen:
                            book_id = self.trainset.to_raw_iid(item_id)
                            top_n[int(self.trainset.to_raw_uid(uiid))].append( (book_id, 0.0) )
                            pos += 1
                            if (pos > 40):
                                break

                print(f'{filter}-based, {metric} and {algorithm}')
                print(f'HIT RATE: ', RecommenderMetrics.hit_rate(top_n, left_out_test_set))
                print(f'USER COVERAGE: ', RecommenderMetrics.user_coverage(top_n, eval_data.get_full_trainset().n_users))
                print(f'DIVERSITY: ', RecommenderMetrics.diversity(top_n, model.fit(eval_data.get_full_trainset()) ))
                print(f'NOVELTY: ', RecommenderMetrics.novelty(top_n, eval_data.get_popularity_rankings()))
                print('')
