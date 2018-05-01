import pprint

from pymongo import MongoClient


def docs_insert(db, collection_name, documents):
    if collection_name in db.collection_names():
        db.drop_collection(collection_name)
    result = db[collection_name].insert_many(documents)
    pprint.pprint(list(result.inserted_ids))


def resolve(db, collection_name, pipeline):
    result = db[collection_name].aggregate(pipeline)
    pprint.pprint(list(result))


client = MongoClient("localhost", 27017)
db = client.aggregationExample
