from MongoDB.pymongodbExamples.setup.setup import db, docs_insert, resolve

"""
$project接受上一个stage传递的documents并过滤或添加document中的域传递给下一个stage。
"""


def include_specific_fields():
    books = [
        {
            "_id": 1,
            "title": "abc123",
            "isbn": "0001122223334",
            "author": {"last": "zzz", "first": "aaa"},
            "copies": 5
        }
    ]

    pipeline = [
        {"$project": {"title": 1, "author": 1}}
    ]

    docs_insert(db, "books", books)
    resolve(db, "books", pipeline)


def suppress_id_field():
    books = [
        {
            "_id": 1,
            "title": "abc123",
            "isbn": "0001122223334",
            "author": {"last": "zzz", "first": "aaa"},
            "copies": 5
        }
    ]

    pipeline = [
        {"$project": {"_id": 0, "title": 1, "author": 1}}
    ]

    docs_insert(db, "books", books)
    resolve(db, "books", pipeline)


def exclude_fields_from_embedded_documents():
    books = [
        {
            "_id": 1,
            "title": "abc123",
            "isbn": "0001122223334",
            "author": {"last": "zzz", "first": "aaa"},
            "copies": 5,
            "lastModified": "2016-07-28"
        }
    ]

    pipeline = [
        {"$project": {"author.first": 0, "lastModified": 0}}
    ]

    docs_insert(db, "books", books)
    resolve(db, "books", pipeline)


def conditionally_exclude_fields():
    books = [
        {
            "_id": 1,
            "title": "abc123",
            "isbn": "0001122223334",
            "author": {"last": "zzz", "first": "aaa"},
            "copies": 5,
            "lastModified": "2016-07-28"
        },
        {
            "_id": 2,
            "title": "Baked Goods",
            "isbn": "9999999999999",
            "author": {"last": "xyz", "first": "abc", "middle": ""},
            "copies": 2,
            "lastModified": "2017-07-21"
        },
        {
            "_id": 3,
            "title": "Ice Cream Cakes",
            "isbn": "8888888888888",
            "author": {"last": "xyz", "first": "abc", "middle": "mmm"},
            "copies": 5,
            "lastModified": "2017-07-22"
        }
    ]

    pipeline = [
        {
            "$project": {
                "title": 1,
                "author.first": 1,
                "author.last": 1,
                "author.middle": {
                    "$cond": {
                        "if": {"$eq": ["", "$author.middle"]},
                        "then": "$$REMOVE",
                        "else": "$author.middle"
                    }
                }
            }
        }
    ]

    docs_insert(db, "books", books)
    resolve(db, "books", pipeline)


def include_computed_fields():
    # TODO include_computed_fields()
    pass


if __name__ == '__main__':
    exclude_fields_from_embedded_documents()
