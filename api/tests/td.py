from yaml import dump

category1 = {"id": 1, "name": "category1"}
category2 = {"id": 1, "name": "category2"}
category3 = {"id": 1, "name": "category3"}
goods1 = {
    "id": 1,
    "category": 1,
    "model": "model1",
    "name": "name1",
    "price": 100,
    "price_rrc": 110,
    "quantity": 4,
    "parameters": {"name1": "v1", "name2": "v2"},
}

base_yaml = dump({"shop": "shop", "categories": [category1], "goods": [goods1]})

not_shop_owner_yaml = dump(
    {"shop": "not owner", "categories": [category1], "goods": [goods1]}
)
