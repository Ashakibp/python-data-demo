from pymongo import MongoClient


PORT = 27017
MONGO_CONNECTION_STRING = "localhost"

class collection_manager(object):
    def __init__(self, db_name, collection_name):
        client = MongoClient(MONGO_CONNECTION_STRING, PORT)
        self.db = client[db_name]
        self.collection = self.db.get_collection(collection_name)

    def find_query(self, query):
        r_query = []
        l = self.collection.find(query)
        for x in l:
            r_query.append(x)
        return r_query

    def insert_query(self, query):
        self.collection.insert(query)

    def create_collection(self, collection_name):
        self.db.create_collection(collection_name)

    def create_index(self, column):
        self.collection.create_index(column)

    def create_indexes(self):
        self.collection.create_indexes()

    def change_collection(self, name):
        self.collection = self.db.get_collection(name)

    def update_query(self, query1, query2):
        self.collection.update(query1, query2)

    def add_query(self, query):
        self.collection.save(query)
