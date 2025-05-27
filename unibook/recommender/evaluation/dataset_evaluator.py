from surprise.model_selection import train_test_split
from surprise.model_selection import LeaveOneOut
from surprise import KNNBaseline

class DatasetEvaluator:
    """Dataset evaluator that gives the different types of trainset and testset."""

    def __init__(self, data, popularity_rankings):
        """Initialise the train and test set."""

        self.rankings = popularity_rankings

        #Build a full training set for evaluating overall properties
        self.full_trainset = data.build_full_trainset()
        self.full_anti_testset = self.full_trainset.build_anti_testset()

        #Build a 75/25 train/test split for measuring accuracy
        self.trainset, self.testset = train_test_split(data, test_size=.25, random_state=1)

        # Build a "leave one out" train/test split for evaluating top-N recommenders
        # And build an anti-test-set for building predictions
        LOOCV = LeaveOneOut(n_splits=1, random_state=1)
        for train, test in LOOCV.split(data):
            self.LOOCV_train = train
            self.LOOCV_test = test

        self.LOOCV_anti_testset = self.LOOCV_train.build_anti_testset()

    def get_full_trainset(self):
        """Get the full train set."""

        return self.full_trainset

    def get_full_anti_testset(self):
        """Get the full anti test set."""

        return self.full_anti_testset

    def get_anti_testset_for_user(self, user_id):
        """Get the anti test set for a user."""

        trainset = self.full_trainset
        fill = trainset.global_mean
        anti_testset = []
        user_inner_id = trainset.to_inner_uid(str(user_id))
        user_items = set([j for (j, _) in trainset.ur[user_inner_id]])
        anti_testset += [(trainset.to_raw_uid(user_inner_id), trainset.to_raw_iid(item), fill) for
                                 item in trainset.all_items() if
                                 item not in user_items]
        return anti_testset

    def get_trainset(self):
        """Get the train set."""

        return self.trainset

    def get_testset(self):
        """Get the test set."""

        return self.testset

    def get_LOOCV_trainset(self):
        """Get the leave one out cross validation train set."""

        return self.LOOCV_train

    def get_LOOCV_testset(self):
        """Get the leave one out cross validation test set."""

        return self.LOOCV_test

    def get_LOOCV_anti_testset(self):
        """Get the leave one out cross validation anti test set."""

        return self.LOOCV_anti_testset

    def get_popularity_rankings(self):
        """Get the popularity rankings."""

        return self.rankings
