import itertools

from surprise import accuracy
from collections import defaultdict

class RecommenderMetrics:
    """Class that gets the different types of metrics for the recommender."""

    def mae(predictions):
        """Get the mae of the predictions."""

        return accuracy.mae(predictions, verbose=False)

    def rmse(predictions):
        """Get the rmse of the predictions."""

        return accuracy.rmse(predictions, verbose=False)

    def get_top_n(predictions, n=10, minimum_rating=9.0):
        """Get the top n predictions with the minimum rating provided."""

        top_n = defaultdict(list)

        for user_id, book_id, actual_rating, estimated_rating, _ in predictions:
            if (estimated_rating >= minimum_rating):
                top_n[int(user_id)].append((book_id, estimated_rating))

        for user_id, ratings in top_n.items():
            ratings.sort(key=lambda x: x[1], reverse=True)
            top_n[int(user_id)] = ratings[:n]

        return top_n

    def hit_rate(top_n_predicted, left_out_predictions):
        """Get the hit rate of the predictions."""

        hits = 0
        total = 0

        # For each left-out rating
        for left_out in left_out_predictions:
            user_id = left_out[0]
            left_out_book_id = left_out[1]
            # Is it in the predicted top 10 for this user?
            hit = False
            for book_id, predicted_rating in top_n_predicted[int(user_id)]:
                if (left_out_book_id == book_id):
                    hit = True
                    break
            if (hit) :
                hits += 1

            total += 1

        # Compute overall precision
        return hits/total

    def cumulative_hit_rate(top_n_predicted, left_out_predictions, rating_cut_off=0):
        """Get the cumulative hit rate of the predictions."""

        hits = 0
        total = 0

        # For each left-out rating
        for user_id, left_out_book_id, actual_rating, estimated_rating, _ in left_out_predictions:
            # Only look at ability to recommend things the users actually liked...
            if (actual_rating >= rating_cut_off):
                # Is it in the predicted top 10 for this user?
                hit = False
                for book_id, predicted_rating in top_n_predicted[int(user_id)]:
                    if (left_out_book_id == book_id):
                        hit = True
                        break
                if (hit) :
                    hits += 1

                total += 1

        # Compute overall precision
        return hits/total

    def rating_hit_rate(top_n_predicted, left_out_predictions):
        """Get the rating hit rate of the predictions."""

        hits = defaultdict(float)
        total = defaultdict(float)

        # For each left-out rating
        for user_id, left_out_book_id, actual_rating, estimated_rating, _ in left_out_predictions:
            # Is it in the predicted top N for this user?
            hit = False
            for book_id, predicted_rating in top_n_predicted[int(user_id)]:
                if (left_out_book_id == book_id):
                    hit = True
                    break
            if (hit) :
                hits[actual_rating] += 1

            total[actual_rating] += 1

        # Compute overall precision
        for rating in sorted(hits.keys()):
            print (rating, hits[rating] / total[rating])

    def average_reciprocal_hit_rank(top_n_predicted, left_out_predictions):
        """Get the average reciprocal hit rank of the predictions."""

        summation = 0
        total = 0
        # For each left-out rating
        for user_id, left_out_book_id, actual_rating, estimated_rating, _ in left_out_predictions:
            # Is it in the predicted top N for this user?
            hit_rank = 0
            rank = 0
            for book_id, predicted_rating in top_n_predicted[int(user_id)]:
                rank = rank + 1
                if (left_out_book_id == book_id):
                    hit_rank = rank
                    break
            if (hit_rank > 0) :
                summation += 1.0 / hit_rank

            total += 1

        return summation / total

    def user_coverage(top_n_predicted, num_users, rating_threshold=0):
        """Get the percentage of users that have at least one 'good' recommendation."""

        hits = 0
        for user_id in top_n_predicted.keys():
            hit = False
            for book_id, predicted_rating in top_n_predicted[user_id]:
                if (predicted_rating >= rating_threshold):
                    hit = True
                    break
            if (hit):
                hits += 1

        return hits / num_users

    def diversity(top_n_predicted, sims_algo):
        """Get the diversity of the predictions."""

        n = 0
        total = 0
        sims_matrix = sims_algo.compute_similarities()
        for user_id in top_n_predicted.keys():
            pairs = itertools.combinations(top_n_predicted[user_id], 2)
            for pair in pairs:
                book1 = pair[0][0]
                book2 = pair[1][0]
                inner_id1 = sims_algo.trainset.to_inner_iid(str(book1))
                inner_id2 = sims_algo.trainset.to_inner_iid(str(book2))
                similarity = sims_matrix[inner_id1][inner_id2]
                total += similarity
                n += 1

        S = total / n
        return (1-S)

    def novelty(top_n_predicted, rankings):
        """Get the novelty of the predictions."""

        n = 0
        total = 0
        for user_id in top_n_predicted.keys():
            for rating in top_n_predicted[user_id]:
                book_id = rating[0]
                rank = rankings[book_id]
                total += rank
                n += 1
        return total / n
