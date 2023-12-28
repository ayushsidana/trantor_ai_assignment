import os
from sqlmodel import Session, create_engine
from sqlmodel.pool import StaticPool
from trantor_ai_assignment.settings import DATABASE_URL

# DATABASE_URL="sqlite:///./test.db"
engine = create_engine(DATABASE_URL, connect_args={"check_same_thread": False}, poolclass=StaticPool)

def get_session() -> Session:
    with Session(engine) as session:
        yield session
