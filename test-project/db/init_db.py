from db.base_class import Base
from db.session import engine


if __name__ == '__main__':
    Base.metadata.create_all(bind=engine)
