import copy
from typing import List, Union

from sqlalchemy import Column, String, TIMESTAMP, Boolean, func
from sqlalchemy.dialects.mysql import INTEGER
from sqlalchemy.ext.declarative import as_declarative, declared_attr


@as_declarative()
class Base:
    id = Column(INTEGER(unsigned=True), primary_key=True, index=True, autoincrement=True)
    created_at = Column(TIMESTAMP, server_default=func.now(), comment='create time of the record')
    updated_at = Column(TIMESTAMP, server_default=func.now(), onupdate=func.now(),
                        comment='update time of the record')
    deleted = Column(Boolean, default=False, comment='delete flag')
    __name__: str

    # Automatically assigns a table name that is lowercase for the current class name
    @declared_attr
    def __tablename__(cls) -> str:
        table_name = []
        class_name = cls.__name__
        for index, char in enumerate(class_name):
            if char.isupper() and index != 0:
                table_name.append("_")
            table_name.append(char)
        return ''.join(table_name).lower()

    # set engine
    @declared_attr
    def __table_args__(self) -> dict:
        return {'mysql_engine': 'InnoDB'}


class UserBase(Base):
    __abstract__ = True

    _groups = Column(String(255), default='', comment='user groups')

    @property
    def groups(self) -> List[str]:
        return [group for group in self._groups.split(',')] if self._groups else []

    @groups.setter
    def groups(self, value: List[str] = None) -> None:
        self._groups = ','.join([groups.replace(' ', '') for groups in value]) if value else ''

    def group_add(self, value: Union[str, List[str]]) -> None:
        """ Add groups for users """
        values = value if isinstance(value, list) else [value]
        tmp_groups = copy.deepcopy(self.groups)
        for value in values:
            if value not in tmp_groups:
                tmp_groups.append(value)
        self.groups = tmp_groups

    def group_remove(self, value: Union[str]) -> None:
        """ Delete groups for users """
        values = value if isinstance(value, list) else [value]
        groups = copy.deepcopy(self.groups)
        for value in values:
            if value in groups:
                groups.remove(value)
        self.groups = groups
