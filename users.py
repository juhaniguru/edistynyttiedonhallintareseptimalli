import contextlib
import datetime
import logging
import uuid
from random import choice

from passlib.context import CryptContext
from faker import Faker
from sqlalchemy import text

from db import get_db

logging.getLogger('passlib').setLevel(logging.ERROR)


def get_users(_db):
    user_ids = []

    _query = "SELECT id FROM users"
    rows = _db.execute(text(_query))
    for row in rows:
        user_ids.append(row[0])

    return user_ids


def insert_roles():
    with get_db() as _db:
        for r in ['normaluser', 'admin', 'moderator']:
            try:
                _query = "INSERT INTO auth_roles(role) VALUES(:role)"
                _db.execute(text(_query), {'role': r})
                _db.commit()
            except Exception as e:
                print(e)
                _db.rollback()


def _get_roles(_db):
    roles_ids = []

    _query = "SELECT id FROM auth_roles"

    rows = _db.execute(text(_query))
    for r in rows:
        roles_ids.append(r[0])

    return roles_ids


def insert_users(num_of_users=1000):
    bcrypt_context = CryptContext(schemes=['bcrypt'], deprecated='auto')

    fake = Faker()
    with get_db() as _db:
        role_ids = _get_roles(_db)
        _query = "INSERT INTO users(username, password, auth_role_id) VALUES"
        variables = {}
        start = datetime.datetime.now()
        for i in range(num_of_users):
            pwd = bcrypt_context.hash('salasana')
            _random_str = str(uuid.uuid4())
            _query += f"(:username{i}, :password{i}, :role{i}),"
            variables[f'username{i}'] = f'{fake.first_name()}-{_random_str}'
            variables[f'password{i}'] = pwd
            variables[f'role{i}'] = choice(role_ids)

        _query = _query[:-1]

        _db.execute(text(_query), variables)
        _db.commit()
        end = datetime.datetime.now()
        print("########### aikaa kului:", end - start)
