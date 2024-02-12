from random import choice, randint

import faker_food
from sqlalchemy import text

from categories import get_categories
from db import get_db
from users import get_users

from faker import Faker
from faker_food import FoodProvider


def _get_ingredients(_db):
    _query = "SELECT id FROM ingredients"
    ingredient_ids = []
    rows = _db.execute(text(_query))
    for row in rows:
        ingredient_ids.append(row[0])

    return ingredient_ids


def _get_recipes(_db):
    _query = "SELECT id FROM recipe"
    recipe_ids = []
    rows = _db.execute(text(_query))
    for row in rows:
        recipe_ids.append(row[0])

    return recipe_ids


def _get_states(_db):
    _query = "SELECT id FROM states"
    state_ids = []
    rows = _db.execute(text(_query))
    for row in rows:
        state_ids.append(row[0])

    return state_ids


def insert_states():
    with get_db() as _db:
        for s in ['private', 'public']:
            try:
                _query = "INSERT INTO states(state) VALUES(:state)"
                _db.execute(text(_query), {'state': s})
                _db.commit()
            except Exception as e:
                print(e)
                _db.rollback()


def insert_recipes():
    fake = Faker()
    fake.add_provider(FoodProvider)
    with get_db() as _db:
        user_ids = get_users(_db)
        state_ids = _get_states(_db)
        category_ids = get_categories(_db)
        _query = "INSERT INTO recipe(name, description, created_at, user_id, state_id, category_id) VALUES"
        variables = {}
        for i in range(5000):
            _query += f'(:name{i}, :description{i}, :created_at{i}, :user_id{i}, :state_id{i},:category_id{i}),'
            variables[f'name{i}'] = fake.dish()
            variables[f'description{i}'] = fake.text()
            variables[f'created_at{i}'] = fake.date()
            variables[f'user_id{i}'] = choice(user_ids)
            variables[f'state_id{i}'] = choice(state_ids)
            variables[f'category_id{i}'] = choice(category_ids)

        _query = _query[:-1]
        _db.execute(text(_query), variables)
        _db.commit()


def insert_ingredients():
    with get_db() as _db:
        for ingredient in faker_food.ingredients:
            try:
                _query = "INSERT INTO ingredients(ingredient) VALUES(:ingredient)"
                _db.execute(text(_query), {'ingredient': ingredient})
                _db.commit()
            except Exception as e:
                _db.rollback()


def mix_ingredients_and_recipes():
    fake = Faker()
    fake.add_provider(FoodProvider)
    with get_db() as _db:
        recipe_ids = _get_recipes(_db)
        ingredient_ids = _get_ingredients(_db)
        _query = "INSERT INTO recipe_has_ingredients(recipe_id, ingredients_id, amount) VALUES(:recipe_id, :ingredient_id, :amount)"
        for i in range(1000):
            try:

                _db.execute(text(_query), {'recipe_id': choice(recipe_ids), 'ingredient_id': choice(ingredient_ids),
                                           'amount': f'{fake.measurement_size()} {fake.metric_measurement()}'})
                _db.commit()
            except Exception as e:
                print(e)
                _db.rollback()


def _get_rating():
    x = randint(1, 4)
    y = randint(1, 9) / 10

    return round(x+y, 1)


def get_cooking():
    fake = Faker()
    with get_db() as _db:
        users = get_users(_db)
        recipes = _get_recipes(_db)
        _query = f"INSERT INTO cooking(cooked_date, user_id, recipe_id, rating) VALUES"
        variables = {}
        for i in range(7000):
            _query += f"(:cooked_date{i}, :user_id{i}, :recipe_id{i}, :rating{i}),"
            variables[f'cooked_date{i}'] = fake.date()
            variables[f'user_id{i}'] = choice(users)
            variables[f'recipe_id{i}'] = choice(recipes)
            variables[f'rating{i}'] = _get_rating()
        _query = _query[:-1]

        _db.execute(text(_query), variables)
        _db.commit()
