from bson import Decimal128
from bson.son import SON
from pymongo import MongoClient
import pprint

client = MongoClient("localhost", 27017)
db = client.aggregationExample

documents = [
    {"_id": 1, "title": "The Pillars of Society", "artist": "Grosz", "year": 1926,
     "price": Decimal128("199.99")},
    {"_id": 2, "title": "Melancholy III", "artist": "Munch", "year": 1902,
     "price": Decimal128("280.00")},
    {"_id": 3, "title": "Dancer", "artist": "Miro", "year": 1925,
     "price": Decimal128("76.04")},
    {"_id": 4, "title": "The Great Wave off Kanagawa", "artist": "Hokusai",
     "price": Decimal128("167.30")},
    {"_id": 5, "title": "The Persistence of Memory", "artist": "Dali", "year": 1931,
     "price": Decimal128("483.00")},
    {"_id": 6, "title": "Composition VII", "artist": "Kandinsky", "year": 1913,
     "price": Decimal128("385.00")},
    {"_id": 7, "title": "The Scream", "artist": "Munch", "year": 1893},
    {"_id": 8, "title": "Blue Flower", "artist": "O'Keefe", "year": 1918,
     "price": Decimal128("118.42")}
]

result = db.artwork.insert_many(documents)
pprint.pprint(result.inserted_ids)

'''
$bucket
分区间后聚合
pandas.cut()
pandas.qcut()
'''
pipeline = [
    {
        '$bucket': {
            'groupBy': '$price',
            'boundaries': [0, 200, 400],
            'default': 'Other',
            'output': {
                'count': {'$sum': 1},
                'titles': {'$push': '$title'}
            }
        }
    }
]

pprint.pprint(list(db.artwork.aggregate(pipeline)))
