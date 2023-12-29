from contextlib import contextmanager
from sqlmodel import SQLModel, Session, create_engine
from .settings import DATABASE_URL

engine = create_engine(DATABASE_URL)

@contextmanager
def get_session() -> Session:
    session = Session(engine)
    try:
        yield session
    finally:
        session.close()

def create_db_and_tables():
    SQLModel.metadata.create_all(engine)

