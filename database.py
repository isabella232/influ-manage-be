from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from contextlib import contextmanager, AbstractContextManager
from typing import Callable, Any

from sqlalchemy.orm import sessionmaker
from sqlalchemy.orm import Session

from meta.singleton import Singleton

SQLALCHEMY_DATABASE_URL = "sqlite:///./sql_app.db"
ENGINE = create_engine(
    SQLALCHEMY_DATABASE_URL, connect_args={"check_same_thread": False}
)
Base = declarative_base()


class Database(Singleton):
    def __init__(self, engine: Any = ENGINE):

        self.__session_factory = sessionmaker(
            autocommit=False, autoflush=False, bind=engine, expire_on_commit=False)

    @contextmanager
    def session(self) -> Callable[..., AbstractContextManager[Session]]:
        session: Session = self.__session_factory()
        try:
            yield session
        except Exception:
            session.rollback()
            raise
        finally:
            session.close()
