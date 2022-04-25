from passlib.context import CryptContext
from sqlalchemy.orm import Session

from crud import user_crud
from models import User

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")


def get_password_hash(password):
    return pwd_context.hash(password)


def verify_password(plain_password, hashed_password):
    return pwd_context.verify(plain_password, hashed_password)


def authenticate_user(db: Session, username: str, password: str):
    user = user_crud.get_user_by_username(db=db, username=username)
    if not user:
        return False
    if not verify_password(password, user.hashed_password):
        return False
    return user


def fake_decode_token(db: Session, token: str):
    user = db.query(User).filter(User.username == token).first()
    return user
