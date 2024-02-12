import faker_food
from faker import Faker
from faker_food import FoodProvider
from sqlalchemy import text

from db import get_db


def get_categories(_db):
    category_ids = []
    _query = "SELECT id FROM categories"
    rows = _db.execute(text(_query))
    for row in rows:
        category_ids.append(row[0])

    return category_ids


def insert_ethnic_categories():
    with get_db() as _db:
        query = "INSERT INTO categories(name) VALUES"
        variables = {}
        for c, category in enumerate(faker_food.ethnic_categories):
            query += f'(:name{c}),'
            variables[f'name{c}'] = category

        query = query[:-1]
        _db.execute(text(query), variables)
        _db.commit()


def insert_categories():
    with get_db() as _db:
        query = "INSERT INTO categories(name) VALUES"
        variables = {}
        for c, category in enumerate(faker_food.categories):
            query += f'(:name{c}),'
            variables[f'name{c}'] = category

        query = query[:-1]
        _db.execute(text(query), variables)
        _db.commit()
