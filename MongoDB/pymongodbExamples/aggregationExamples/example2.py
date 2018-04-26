from pymongo import MongoClient
from bson.son import SON
import pprint

client = MongoClient("localhost", 27017)
db = client.aggregationExample

# SON类似于OrderedDict，为键值对提供顺序
pipeline = [
    {'$unwind': '$tags'},
    {'$group': {'_id': '$tags', 'count': {'$sum': 1}}},
    {'$sort': SON([('count', -1), ('_id', -1)])}
]

# pprint.pprint(list(db.products.aggregate(pipeline)))

pprint.pprint(db.command('aggregate', 'products', pipeline=pipeline, explain=True))
