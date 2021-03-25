from typing import Generator

from db.session import SessionFactory


def get_session() -> Generator:
    """
    get database session
    """
    db = SessionFactory()
    try:
        yield db
    finally:
        db.close()
