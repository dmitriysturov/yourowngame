from app.db.base import Base
from app.db.session import engine
from app.models import *  # noqa: F401,F403


def create_tables() -> None:
    Base.metadata.create_all(bind=engine)
