from MongoDB.pymongodbExamples.setup.setup import db, docs_insert, resolve
from bson import Decimal128

documents = [
    {"_id": 1, "title": "The Pillars of Society", "artist": "Grosz", "year": 1926,
     "price": Decimal128("199.99"),
     "tags": ["painting", "satire", "Expressionism", "caricature"]},
    {"_id": 2, "title": "Melancholy III", "artist": "Munch", "year": 1902,
     "price": Decimal128("280.00"),
     "tags": ["woodcut", "Expressionism"]},
    {"_id": 3, "title": "Dancer", "artist": "Miro", "year": 1925,
     "price": Decimal128("76.04"),
     "tags": ["oil", "Surrealism", "painting"]},
    {"_id": 4, "title": "The Great Wave off Kanagawa", "artist": "Hokusai",
     "price": Decimal128("167.30"),
     "tags": ["woodblock", "ukiyo-e"]},
    {"_id": 5, "title": "The Persistence of Memory", "artist": "Dali", "year": 1931,
     "price": Decimal128("483.00"),
     "tags": ["Surrealism", "painting", "oil"]},
    {"_id": 6, "title": "Composition VII", "artist": "Kandinsky", "year": 1913,
     "price": Decimal128("385.00"),
     "tags": ["oil", "painting", "abstract"]},
    {"_id": 7, "title": "The Scream", "artist": "Munch", "year": 1893,
     "tags": ["Expressionism", "painting", "oil"]},
    {"_id": 8, "title": "Blue Flower", "artist": "O'Keefe", "year": 1918,
     "price": Decimal128("118.42"),
     "tags": ["abstract", "painting"]}
]

pipeline = [{
    "$facet": {
        "categorizedByTags": [
            {"$unwind": "$tags"},
            {"$sortByCount": "$tags"}
        ],

        "categorizedByPrice": [
            {"$match": {"price": {"$exists": 1}}},
            {"$bucket": {
                "groupBy": "$price",
                "boundaries": [0, 150, 200, 300, 400],
                "default": "Other",
                "output": {
                    "count": {"$sum": 1},
                    "titles": {"$push": "$title"}
                }
            }}
        ],

        "categorizedByYears(Auto)": [{
            "$bucketAuto": {
                "groupBy": "$year",
                "buckets": 4
            }
        }]
    }
}]

if __name__ == '__main__':
    docs_insert(db, "artwork", documents)
    resolve(db, "artwork", pipeline)
