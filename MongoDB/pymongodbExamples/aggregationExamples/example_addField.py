from MongoDB.pymongodbExamples.setup.setup import db
from pymongo import MongoClient
import pprint

"""
$addField
update({}, {'$set': {}})
"""


def docs_insert():
    documents = [
        {
            '_id': 1,
            'student': "Maya",
            'homework': [10, 5, 10],
            'quiz': [10, 8],
            'extraCredit': 0
        },
        {
            '_id': 2,
            'student': "Ryan",
            'homework': [5, 6, 5],
            'quiz': [8, 8],
            'extraCredit': 8
        }
    ]

    result = db.scores.insert_many(documents)
    pprint.pprint(result.inserted_id)


def resolve():
    pipeline = [
        {
            '$addFields': {
                'totalHomework': {'$sum': '$homework'},
                'totalQuiz': {'$sum': '$quiz'}
            }
        },
        {
            '$addFields': {
                'totalScore': {'$add': ['$totalHomework', '$totalQuiz', '$extraCredit']}
            }
        }
    ]

    pprint.pprint(list(db.scores.aggregate(pipeline)))

    '''
    Adding Fields to an Embedded Document
    '''
    db.vehicles.insert_many([
        {'_id': 1, 'type': "car", 'specs': {'doors': 4, 'wheels': 4}},
        {'_id': 2, 'type': "motorcycle", 'specs': {'doors': 0, 'wheels': 2}},
        {'_id': 3, 'type': "jet ski"}
    ])

    pipeline = [
        {
            '$addFields': {
                'specs.fuel_type': 'unleaded'
            }
        }
    ]

    pprint.pprint(list(db.vehicles.aggregate(pipeline)))

    '''
    Overwriting an existing field
    '''
    document = {'_id': 1, 'dogs': 10, 'cats': 15}

    db.animals.insert_one(document)

    pipeline = [
        {'$addFields': {'cats': 20}}
    ]

    pprint.pprint(list(db.animals.aggregate(pipeline)))
