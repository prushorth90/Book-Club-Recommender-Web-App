import sys
sys.path.append("unibook")

from recommender.book_data import BookData
from dataset_evaluator import DatasetEvaluator
from algorithm_evaluator import AlgorithmEvaluator

class RecommenderEvaluator:
    """Evaluator that evaluates each algorithm added."""

    algorithms = []

    def __init__(self):
        """Initialise the data evaluator."""

        books = BookData()
        print("Loading book ratings...")
        data = books.load_book_data()
        print("\nComputing book popularity ranks so we can measure novelty later...")
        rankings = books.get_popularity_ranks()
        self.dataset_evaluator = DatasetEvaluator(data, rankings)

    def add_algorithm(self, algorithm, name):
        """Add the given algorithm to the algorithms that needs to be evaluated."""

        alg = AlgorithmEvaluator(algorithm, name)
        self.algorithms.append(alg)

    def evaluate(self, do_top_n):
        """Evaluate all the algorithms provided"""

        results = {}
        for algorithm in self.algorithms:
            print("Evaluating ", algorithm.get_name(), "...")
            results[algorithm.get_name()] = algorithm.evaluate(self.dataset_evaluator, do_top_n)

        # Print results
        print("\n")

        if (do_top_n):
            print("{:<10} {:<10} {:<10} {:<10} {:<10} {:<10} {:<10} {:<10} {:<10}".format(
                    "Algorithm", "RMSE", "MAE", "HR", "cHR", "ARHR", "Coverage", "Diversity", "Novelty"))
            for (name, metrics) in results.items():
                print("{:<10} {:<10.4f} {:<10.4f} {:<10.4f} {:<10.4f} {:<10.4f} {:<10.4f} {:<10.4f} {:<10.4f}".format(
                        name, metrics["RMSE"], metrics["MAE"], metrics["HR"], metrics["cHR"], metrics["ARHR"],
                                      metrics["Coverage"], metrics["Diversity"], metrics["Novelty"]))
        else:
            print("{:<10} {:<10} {:<10}".format("Algorithm", "RMSE", "MAE"))
            for (name, metrics) in results.items():
                print("{:<10} {:<10.4f} {:<10.4f}".format(name, metrics["RMSE"], metrics["MAE"]))

        print("\nLegend:\n")
        print("RMSE:      Root Mean Squared Error. Lower values mean better accuracy.")
        print("MAE:       Mean Absolute Error. Lower values mean better accuracy.")
        if (do_top_n):
            print("HR:        Hit Rate; how often we are able to recommend a left-out rating. Higher is better.")
            print("cHR:       Cumulative Hit Rate; hit rate, confined to ratings above a certain threshold. Higher is better.")
            print("ARHR:      Average Reciprocal Hit Rank - Hit rate that takes the ranking into account. Higher is better." )
            print("Coverage:  Ratio of users for whom recommendations above a certain threshold exist. Higher is better.")
            print("Diversity: 1-S, where S is the average similarity score between every possible pair of recommendations")
            print("           for a given user. Higher means more diverse.")
            print("Novelty:   Average popularity rank of recommended items. Higher means more novel.")
