import contextlib

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker


@contextlib.contextmanager
def get_db():
    _db = None
    try:
        engine = create_engine('mysql+mysqlconnector://root:@localhost/reseptit')
        db_session = sessionmaker(bind=engine)

        _db = db_session()
        yield _db
    except Exception as e:
        print(e)
    finally:
        if _db is not None:
            _db.close()
