from sqlmodel import Session
from .database import engine

# Dependency to get a session
def get_session():
    with Session(engine) as session:
        yield session