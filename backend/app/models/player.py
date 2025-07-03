# Player SQLModel Model
from sqlmodel import Field, SQLModel


class Player(SQLModel, table=True):
    __tablename__ = "players" # type: ignore
    id: int | None = Field(default=None, primary_key=True)
    first_name: str
    last_name: str
    height: str
    position: str
    image_url: str