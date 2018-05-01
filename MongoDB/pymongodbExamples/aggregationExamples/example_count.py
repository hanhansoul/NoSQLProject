from MongoDB.pymongodbExamples.setup.setup import db, docs_insert, resolve

"""
{ $count: <string> }
返回输入到当前$count阶段的文档数量，保存在<string>域中。
"""
documents = [
    {"_id": 1, "subject": "History", "score": 88},
    {"_id": 2, "subject": "History", "score": 92},
    {"_id": 3, "subject": "History", "score": 97},
    {"_id": 4, "subject": "History", "score": 71},
    {"_id": 5, "subject": "History", "score": 79},
    {"_id": 6, "subject": "History", "score": 83}
]

pipeline = [
    {"$match": {
        "score": {
            "$gt": 80
        }
    }},
    {
        "$count": "passing_scores"
    }
]

if __name__ == '__main__':
    docs_insert(db, "scores", documents)
    resolve(db, "scores", pipeline)
