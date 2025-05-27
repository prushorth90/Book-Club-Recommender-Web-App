"""
Spark recommender that recommends items to a user.

The implementation is originally used for movies and it's taken from https://sundog-education.com/RecSys/
The source code has been refactored to a class and functions to fit the application of the project.

The spark recommender is implemented in a way to allow use of other csv file such as movie ratings.
The constructor needs to be changed to load the data if other csv file is used.
"""

from pyspark.sql import SparkSession
from pyspark.ml.evaluation import RegressionEvaluator
from pyspark.ml.recommendation import ALS
from pyspark.sql import Row
from pyspark.sql.functions import regexp_replace, explode
from .book_data import BookData
from pyspark.ml.feature import StringIndexer, IndexToString

class SparkRecommender:
    """Spark recommender that recommends items to a user."""

    def __init__(self):
        self.books = BookData()
        self.books.load_book_data()

        # Start the session of the spark
        self.spark = SparkSession\
            .builder\
            .appName("ALSRecommender")\
            .getOrCreate()

    def stop_session(self):
        """Stop the spark session."""

        self.spark.stop()

    def create_num_id_df(self, dataframe, col):
        """Create a dataframe with numeric id for a column in a dataframe."""

        indexer = StringIndexer(inputCol=col, outputCol=(col + "ID"))
        self.indexer_model = indexer.fit(dataframe)
        num_df = self.indexer_model.transform(dataframe)
        return num_df

    def create_ratings_df(self, ratings_file_path):
        """Read the csv file and create a dataframe"""

        df = self.spark.read.option("header", "true").option("sep", ";").csv(ratings_file_path)

        lines = df.rdd
        initial_rdd = lines.map(lambda p: Row(userId=int(p[0]), item=str(p[1]),
                                             rating=float(p[2])))
        initial_ratings = self.spark.createDataFrame(initial_rdd)

        item_col = initial_ratings.columns[1]
        ratings = self.create_num_id_df(initial_ratings, item_col)

        return ratings

    def split_df(self, df, training_size, test_size):
        """Split the dataframe into training set and testing set."""

        (training, test) = df.randomSplit([training_size, test_size])
        return (training, test)

    def create_ALS(self):
        """Create the ALS algorithm."""

        als = ALS(maxIter=10, regParam=0.01, userCol="userId", itemCol="itemID", ratingCol="rating",
                  coldStartStrategy="drop")
        return als

    def train_model(self, trainset, model):
        """Create and fit the model with a training set."""

        self.model = model.fit(trainset)

    def get_recommendations(self, userID, rec_size=10):
        """Get the top N recommendations for a user."""

        user_recs = self.model.recommendForAllUsers(rec_size)
        user_recs = user_recs.filter(user_recs['userID'] == userID)

        id_converter = IndexToString(inputCol="itemID", outputCol="item").setLabels(self.indexer_model.labels)

        recoms = id_converter.transform(user_recs.select(user_recs["userId"],explode('recommendations')).select('userId', 'col.itemID', 'col.rating'))
        result = [row.item for row in recoms.select('item').collect()]
        return result

    def evaluate(self, ratings_file_path):
        """Evaluate the model using different metrics."""

        ratings = self.create_ratings_df(ratings_file_path)
        (training, test) = self.split_df(ratings, 0.8, 0.2)
        als = self.create_ALS()
        self.train_model(training, als)

        predictions = self.model.transform(test)

        evaluator = RegressionEvaluator(labelCol="rating", predictionCol="prediction")
        rmse = evaluator.evaluate(predictions, {evaluator.metricName: "rmse"})
        mse = evaluator.evaluate(predictions, {evaluator.metricName: "mse"})
        mae = evaluator.evaluate(predictions, {evaluator.metricName: "mae"})
        r2 = evaluator.evaluate(predictions, {evaluator.metricName: "r2"})
        var = evaluator.evaluate(predictions, {evaluator.metricName: "var"})

        print("Root-mean-square error = " + str(rmse))
        print("mean-square error = " + str(mse))
        print("Mean absolute error = " + str(mae))
        print("r^2 metric = " + str(r2))
        print("Explained variance = " + str(var))
