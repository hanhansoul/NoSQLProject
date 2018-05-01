from datetime import datetime

from MongoDB.pymongodbExamples.setup.setup import db, docs_insert, resolve

"""
{ $group: 
    { _id: <expression>, 
    <field1>: { 
        <accumulator1> : <expression1> 
    }, 
    ... } 
}

$sum / $avg / $max / $min
$first / $last
$push / $addToSet
$stdDevPop / $stdDevSamp
"""

fstr = "%Y-%m-%d %H:%M:%S"
documents1 = [
    {"_id": 1, "item": "abc", "price": 10, "quantity": 2, "date": datetime.strptime("2014-03-01 08:00:00", fstr)},
    {"_id": 2, "item": "jkl", "price": 20, "quantity": 1, "date": datetime.strptime("2014-03-01 09:00:00", fstr)},
    {"_id": 3, "item": "xyz", "price": 5, "quantity": 10, "date": datetime.strptime("2014-03-15 09:00:00", fstr)},
    {"_id": 4, "item": "xyz", "price": 5, "quantity": 20, "date": datetime.strptime("2014-04-04 11:21:39", fstr)},
    {"_id": 5, "item": "abc", "price": 10, "quantity": 10, "date": datetime.strptime("2014-04-04 21:23:13", fstr)}
]

pipeline1 = [
    {"$group": {
        "_id": {
            "month": {"$month": "$date"},
            "day": {"$dayOfMonth": "$date"},
            "year": {"$year": "$date"}
        },
        "totalPrice": {
            "$sum": {"$multiply": ["$price", "$quantity"]}
        },
        "averageQuantity": {"$avg": "$quantity"},
        "count": {"$sum": 1}
    }}
]

# retrieve distinct values
pipeline2 = [
    {"$group": {
        "_id": "$item"
    }}
]

documents2 = [
    {"_id": 8751, "title": "The Banquet", "author": "Dante", "copies": 2},
    {"_id": 8752, "title": "Divine Comedy", "author": "Dante", "copies": 1},
    {"_id": 8645, "title": "Eclogues", "author": "Dante", "copies": 2},
    {"_id": 7000, "title": "The Odyssey", "author": "Homer", "copies": 10},
    {"_id": 7020, "title": "Iliad", "author": "Homer", "copies": 10}
]

pipeline3 = [
    {"$group": {
        "_id": "$author",
        "books": {"$push": "$title"}
    }}
]

# $$ROOT表示对应的document
pipeline4 = [
    {"$group": {
        "_id": "$author",
        "books": {"$push": "$$ROOT"}
    }}
]

if __name__ == '__main__':
    docs_insert(db, "sales", documents2)
    resolve(db, "sales", pipeline3)
