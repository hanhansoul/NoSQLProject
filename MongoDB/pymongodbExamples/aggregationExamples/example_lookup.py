from MongoDB.pymongodbExamples.setup.setup import db, docs_insert, resolve

"""
{
   $lookup:
     {
       from: <collection to join>,
       localField: <field from the input documents>,
       foreignField: <field from the documents of the "from" collection>,
       as: <output array field>
     }
}
===

{
   $lookup:
     {
       from: <collection to join>,
       let: { <var_1>: <expression>, …, <var_n>: <expression> },
       pipeline: [ <pipeline to execute on the collection to join> ],
       as: <output array field>
     }
}

SELECT *, <output array field>
FROM collection
WHERE <output array field> IN (SELECT <documents as determined from the pipeline>
                               FROM <collection to join>
                               WHERE <pipeline> );
"""


def single_equality_join():
    orders = [
        {"_id": 1, "item": "almonds", "price": 12, "quantity": 2},
        {"_id": 2, "item": "pecans", "price": 20, "quantity": 1},
        {"_id": 3}
    ]

    inventory = [
        {"_id": 1, "sku": "almonds", "description": "product 1", "instock": 120},
        {"_id": 2, "sku": "bread", "description": "product 2", "instock": 80},
        {"_id": 3, "sku": "cashews", "description": "product 3", "instock": 60},
        {"_id": 4, "sku": "pecans", "description": "product 4", "instock": 70},
        {"_id": 5, "sku": None, "description": "Incomplete"},
        {"_id": 6}
    ]

    pipeline = [
        {"$lookup": {
            "from": "inventory",
            "localField": "item",
            "foreignField": "sku",
            "as": "inventory_docs"
        }}
    ]

    docs_insert(db, "orders", orders)
    docs_insert(db, "inventory", inventory)
    resolve(db, "orders", pipeline)


def join_with_array():
    orders = [
        {"_id": 1, "item": "MON1003", "price": 350, "quantity": 2,
         "specs": ["27 inch", "Retina display", "1920x1080"],
         "type": "Monitor"}
    ]

    inventory = [
        {"_id": 1, "sku": "MON1003", "type": "Monitor", "instock": 120,
         "size": "27 inch", "resolution": "1920x1080"},
        {"_id": 2, "sku": "MON1012", "type": "Monitor", "instock": 85,
         "size": "27 inch", "resolution": "1280x800"},
        {"_id": 3, "sku": "MON1031", "type": "Monitor", "instock": 60,
         "size": "23 inch", "display_type": "LED"}
    ]

    pipeline = [
        {"$lookup": {
            "from": "inventory",
            "localField": "specs",
            "foreignField": "size",
            "as": "inventory_docs"
        }}
    ]

    docs_insert(db, "orders", orders)
    docs_insert(db, "inventory", inventory)
    resolve(db, "orders", pipeline)


def join_with_mergeObject():
    orders = [
        {"_id": 1, "item": "almonds", "price": 12, "quantity": 2},
        {"_id": 2, "item": "pecans", "price": 20, "quantity": 1}
    ]

    items = [
        {"_id": 1, "item": "almonds", "description": "almond clusters", "instock": 120},
        {"_id": 2, "item": "bread", "description": "raisin and nut bread", "instock": 80},
        {"_id": 3, "item": "pecans", "description": "candied pecans", "instock": 60}
    ]

    pipeline = [
        {"$lookup": {
            "from": "items",
            "localField": "item",
            "foreignField": "item",
            "as": "fromItems"
        }},
        {"$replaceRoot": {
            "newRoot": {
                "$mergeObjects": [
                    {"$arrayElemAt": ["$fromItems", 0]}
                ]
            }
        }},
        # {"$project": {
        #     "fromItems": 0
        # }}
    ]

    docs_insert(db, "orders", orders)
    docs_insert(db, "items", items)
    resolve(db, "orders", pipeline)


def join_with_multiple_conditions():
    orders = [
        {"_id": 1, "item": "almonds", "price": 12, "ordered": 2},
        {"_id": 2, "item": "pecans", "price": 20, "ordered": 1},
        {"_id": 3, "item": "cookies", "price": 10, "ordered": 60}
    ]

    warehouses = [
        {"_id": 1, "stock_item": "almonds", "warehouse": "A", "instock": 120},
        {"_id": 2, "stock_item": "pecans", "warehouse": "A", "instock": 80},
        {"_id": 3, "stock_item": "almonds", "warehouse": "B", "instock": 60},
        {"_id": 4, "stock_item": "cookies", "warehouse": "B", "instock": 40},
        {"_id": 5, "stock_item": "cookies", "warehouse": "A", "instock": 80}
    ]

    pipeline = [
        {"$lookup": {
            "from": "warehouses",
            "let": {"order_item": "$item",
                    "order_qty": "$ordered"},
            "pipeline": [
                {"$match":
                    {"$expr":
                        {"$and":
                            [
                                {"$eq": ["$stock_item", "$$order_item"]},
                                {"$gte": ["$instock", "$$order_qty"]}
                            ]}}},
                {"$project": {"stock_item": 0, "_id": 0}}
            ],
            "as": "stockdata"
        }}
    ]

    docs_insert(db, "orders", orders)
    docs_insert(db, "warehouses", warehouses)
    resolve(db, "orders", pipeline)


if __name__ == '__main__':
    join_with_multiple_conditions()
