from pymongo import MongoClient

client = MongoClient("localhost", 27017)
db = client.pythondb

db.inventory.insert_one(
    {
        "item": "canvas",
        "qty": 100,
        "tags": ["cotton"],
        "size": {"h": 28, "w": 35.5, "uom": "cm"}
    }
)

# cursor = db.inventory.find({"item": "canvas"})

