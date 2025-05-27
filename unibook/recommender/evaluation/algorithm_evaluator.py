from recommender_metrics import RecommenderMetrics

class AlgorithmEvaluator:
    """Evaluator that evaluates an algorithm with different metrics."""

    def __init__(self, algorithm, name):
        """Initialise the algorithm and name of the algorithm."""

        self.algorithm = algorithm
        self.name = name

    def get_similarities_algo(self, full_trainset):
        """Get the similarities algorithm."""

        return self.algorithm.fit(full_trainset)

    def evaluate(self, dataset_evaluator, do_top_n, n=10, verbose=True):
        """Evaluate the algorithm."""

        metrics = {}
        # Compute accuracy
        if (verbose):
            print("Evaluating accuracy...")
        self.algorithm.fit(dataset_evaluator.get_trainset())
        predictions = self.algorithm.test(dataset_evaluator.get_testset())
        metrics["RMSE"] = RecommenderMetrics.rmse(predictions)
        metrics["MAE"] = RecommenderMetrics.mae(predictions)

        if (do_top_n):
            # Evaluate top-10 with Leave One Out testing
            if (verbose):
                print("Evaluating top-N with leave-one-out...")
            self.algorithm.fit(dataset_evaluator.get_LOOCV_trainset())
            left_out_predictions = self.algorithm.test(dataset_evaluator.get_LOOCV_testset())
            # Build predictions for all ratings not in the training set
            all_predictions = self.algorithm.test(dataset_evaluator.get_LOOCV_anti_testset())
            # Compute top 10 recs for each user
            top_n_predicted = RecommenderMetrics.get_top_n(all_predictions, n)
            if (verbose):
                print("Computing hit-rate and rank metrics...")
            # See how often we recommended a book the user actually rated
            metrics["HR"] = RecommenderMetrics.hit_rate(top_n_predicted, left_out_predictions)
            # See how often we recommended a book the user actually liked
            metrics["cHR"] = RecommenderMetrics.cumulative_hit_rate(top_n_predicted, left_out_predictions)
            # Compute ARHR
            metrics["ARHR"] = RecommenderMetrics.average_reciprocal_hit_rank(top_n_predicted, left_out_predictions)

            #Evaluate properties of recommendations on full training set
            if (verbose):
                print("Computing recommendations with full data set...")
            self.algorithm.fit(dataset_evaluator.get_full_trainset())
            all_predictions = self.algorithm.test(dataset_evaluator.get_full_anti_testset())
            top_n_predicted = RecommenderMetrics.get_top_n(all_predictions, n)
            if (verbose):
                print("Analyzing coverage, diversity, and novelty...")
            # Print user coverage with a minimum predicted rating of 9.0:
            metrics["Coverage"] = RecommenderMetrics.user_coverage(top_n_predicted,
                                                                  dataset_evaluator.get_full_trainset().n_users,
                                                                  rating_threshold=9.0)
            # Measure diversity of recommendations:
            metrics["Diversity"] = RecommenderMetrics.diversity(top_n_predicted, self.get_similarities_algo(dataset_evaluator.get_full_trainset()))

            # Measure novelty (average popularity rank of recommendations):
            metrics["Novelty"] = RecommenderMetrics.novelty(top_n_predicted,
                                                            dataset_evaluator.get_popularity_rankings())

        if (verbose):
            print("Analysis complete.")

        return metrics

    def get_name(self):
        """Get the name of the algorithm."""

        return self.name

    def get_algorithm(self):
        """Get the algorithm"""

        return self.algorithm
