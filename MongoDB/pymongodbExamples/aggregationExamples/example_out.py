from MongoDB.pymongodbExamples.setup.setup import db, docs_insert, resolve

"""
接受来自聚合管道的文档，输出到一个特定的collection中，$out操作符必须是聚合管道的最后一个stage。

如果$out指定的collection已经存在，则会自动替代已有的collection。
"""

books = [
    {"_id": 8751, "title": "The Banquet", "author": "Dante", "copies": 2},
    {"_id": 8752, "title": "Divine Comedy", "author": "Dante", "copies": 1},
    {"_id": 8645, "title": "Eclogues", "author": "Dante", "copies": 2},
    {"_id": 7000, "title": "The Odyssey", "author": "Homer", "copies": 10},
    {"_id": 7020, "title": "Iliad", "author": "Homer", "copies": 10}
]

pipeline = [
    {"$group": {"_id": "$author", "books": {"$push": "$title"}}},
    {"$out": "authors"}
]

docs_insert(db, "books", books)
resolve(db, "books", pipeline)
print(db.authors.find({}))