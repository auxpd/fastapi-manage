from sqlalchemy import Column
from sqlalchemy.dialects.mysql import INTEGER
from sqlalchemy.ext.declarative import as_declarative, declared_attr


@as_declarative()
class Base:
    id = Column(INTEGER(unsigned=True), primary_key=True, index=True, autoincrement=True)
    __name__: str

    # Automatically assigns a table name that is lowercase for the current class name
    @declared_attr
    def __tablename__(cls) -> str:
        return cls.__name__.lower()

    # set engine
    @declared_attr
    def __table_args__(self) -> dict:
        return {'mysql_engine': 'InnoDB'}
