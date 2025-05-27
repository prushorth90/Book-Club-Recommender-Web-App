from recommender_evaluator import RecommenderEvaluator
from surprise import KNNBasic,KNNWithMeans,KNNWithZScore,KNNBaseline,SVD,SVDpp,NormalPredictor
from recommender.algorithms import ContentBasedAlgorithm
from recommender.surprise_recommender import SimpleCollabRecommender
from recommender.spark_recommender import SparkRecommender

class Evaluator:
    """Main class for evaluator that adds algorithm and does the evaluation work."""

    def main():
        """Main function to evaluate the recommender with the specified algorithm."""

        # # BLOCK 1 - Vary KNNBasic and sim-option name parameter- see Evaluation report to see options
        # evaluator = RecommenderEvaluator()
        # userKNN = KNNBasic(sim_options={'name': 'pearson_baseline', 'user_based': True})
        # evaluator.add_algorithm(userKNN, 'userKNN')
        # evaluator.evaluate(True)
        #
        # BLOCK 2 - Vary KNNBasic and sim-option name paraemeter - see Evaluation report to see options
        # evaluator = RecommenderEvaluator()
        # itemKNN = KNNBasic(sim_options={'name': 'pearson_baseline', 'user_based': False})
        # evaluator.add_algorithm(itemKNN, 'itemKNN')
        # evaluator.evaluate(True)
        #
        # BLOCK 3 - User Simple Recommender
        # evaluator = RecommenderEvaluator()
        # simple_recommender = SimpleCollabRecommender()
        # simple_recommender.evaluate('user')
        # evaluator.evaluate(True)
        #
        # BLOCK 4 - Item Simple Recommender
        # evaluator = RecommenderEvaluator()
        # simple_recommender = SimpleCollabRecommender()
        # simple_recommender.evaluate('item')
        # evaluator.evaluate(True)
        #
        # BLOCK 5 - SVD
        # evaluator = RecommenderEvaluator()
        # svd = SVD()
        # evaluator.add_algorithm(svd, 'SVD')
        # evaluator.evaluate(True)
        #
        # BLOCK 6 - SVD++
        # evaluator = RecommenderEvaluator()
        # svdpp = SVDpp()
        # evaluator.add_algorithm(svdpp, 'SVD++')
        # evaluator.evaluate(True)
        #
        # BLOCK 7 - Content
        # evaluator = RecommenderEvaluator()
        # content_based_algorithm = ContentBasedAlgorithm()
        # evaluator.add_algorithm(content_based_algorithm, 'ContentBasedAlgorithm')
        # evaluator.evaluate(True)
        #
        # BLOCK 8 - Spark Recommender
        # recommender = SparkRecommender()
        # ratings = recommender.create_ratings_df('unibook/recommender/book_dataset/BX_Book_Ratings.csv')
        # (training, test) = recommender.split_df(ratings, 0.8, 0.2)
        # als = recommender.create_ALS()
        # recommender.train_model(training, als)
        # recommender.evaluate('unibook/recommender/book_dataset/BX_Book_Ratings.csv')
        #
        # BLOCK 9 - Random
        # evaluator = RecommenderEvaluator()
        # normal_predictor = NormalPredictor()
        # evaluator.add_algorithm(normal_predictor, 'NormalPredictor')
        # evaluator. evaluate(True)


    if __name__ == "__main__":
        main()
