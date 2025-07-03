from sqlmodel import SQLModel, create_engine

# Create database engine and tables
sqlite_file_name = "players.db"
engine = create_engine(f"sqlite:///{sqlite_file_name}", echo=True)

def create_db_and_tables():
    SQLModel.metadata.create_all(engine)