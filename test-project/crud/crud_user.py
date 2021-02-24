from typing import Optional, Union, Dict, Any

from sqlalchemy.orm import Session

import schemas
import models
from .base import CRUDBase
from core.security import get_password_hash, verify_password


class CRUDUser(CRUDBase[models.User, schemas.UserCreate, schemas.UserUpdate]):
    """
    user crud methods
    """
    def get_by_userid(self, db: Session, userid: str) -> Optional[models.User]:
        return db.query(models.User).filter_by(userid=userid).first()

    def create(self, db: Session, obj_in: schemas.UserCreate) -> models.User:
        obj_data = obj_in.dict(exclude_unset=True)
        if 'password' in obj_data.keys():
            obj_data['hashed_password'] = get_password_hash(obj_data['password'])
            del obj_data['password']
        db_obj = self.model(**obj_data)
        db.add(db_obj)
        db.commit()
        db.refresh(db_obj)
        return db_obj

    def update(
            self, db: Session, db_obj: models.User, obj_in: Union[schemas.UserUpdate, Dict[str, Any]]
    ) -> models.User:
        update_data = obj_in if isinstance(obj_in, dict) else obj_in.dict(exclude_unset=True)
        if 'password' in update_data.keys():
            update_data['hashed_password'] = get_password_hash(update_data['password'])
            del update_data['password']
        return super().update(db, db_obj, update_data)

    def authenticate(self, db: Session, userid: str, password: str) -> Optional[models.User]:
        man = db.query(models.User).filter_by(userid=userid).first()
        if not man:
            return None
        if not verify_password(password, man.hashed_password):
            return None
        return man


user = CRUDUser(models.User)
