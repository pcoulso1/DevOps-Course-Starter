import pymongo
from mongo_db.config import Config

class Store:

    def __init__(self):
        self.MONGODB_CLIENT = None
        self.MONGODB_DATABASE = None


    def get_mongodb(self, db_name=Config().MONGO_DEFAULT_DATABASE):
        """
        Returns the MongoDB

        Returns:
            db: The Mongo DB database object.
        """
        if self.MONGODB_DATABASE is None:

            if self.MONGODB_CLIENT is None:
                self.MONGODB_CLIENT = pymongo.MongoClient(Config().MONGO_URL)
            self.MONGODB_DATABASE = self.MONGODB_CLIENT[db_name]

        return self.MONGODB_DATABASE


    def setup_test_store(self):
        """
        Sets a test board ID which is to be used for testing purposes

        Returns:
            None

        """
        self.reset_store()
        self.get_mongodb("testBoard")


    def reset_store(self):
        """
        Resets the test store

        Returns:
            None
        """
        self.MONGODB_DATABASE = None
        self.MONGODB_CLIENT = None
