from contextlib import contextmanager
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, Session
from sqlalchemy.ext.declarative import declarative_base

class Database:
    def __init__(self):
        self._db_url = "sqlite:////D:/PyCharm 2025.3.2.1/projects/DjangoOnFastapi/DjangoOnFastAPI/sqlite.db"
        self._engine = create_engine(self._db_url)
        self._session_factory = sessionmaker(bind=self._engine)

    @contextmanager
    def session(self) -> Session:
        session = self._session_factory()
        try:
            yield session
            session.commit()
        except Exception:
            session.rollback()
            raise
        finally:
            session.close()

database = Database()
Base = declarative_base()