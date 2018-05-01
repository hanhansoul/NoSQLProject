from pymongo import MongoClient

client = MongoClient("localhost", 27017)
db = client.aggregationExample
result = db.products.insert_many([
    {'x': 1, 'tags': ['dog', 'cat']},
    {'x': 2, 'tags': ['cat']},
    {'x': 2, 'tags': ['mouse', 'cat', 'dog']},
    {'x': 3, 'tags': []}
])
print(result.inserted_ids)
