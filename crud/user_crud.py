from typing import Optional
import uuid

from fastapi import HTTPException, status
from sqlalchemy.orm import Session

import utils
from models import User
from schemas import user_schemas


def get_all_users(db: Session):
    users = db.query(User).all()
    return users


def get_user_by_id(db: Session, user_id: int):
    user = db.query(User).filter(User.id == user_id).first()
    if not user:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail='No user with this ID')
    return user


def get_user_by_username(db: Session, username: str):
    user = db.query(User).filter(User.username == username).first()
    if not user:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail='No user with this username')
    return user


def create_user(db: Session, user: user_schemas.UserCreate, is_admin: Optional[bool] = None):
    hashed_password = utils.get_password_hash(user.password)
    new_user = User(**user.dict(exclude={'password'}), hashed_password=hashed_password, id=str(uuid.uuid4()))
    if is_admin:
        new_user.is_superuser = True
        new_user.is_moderator = True
    db.add(new_user)
    db.commit()
    db.refresh(new_user)
    return new_user
