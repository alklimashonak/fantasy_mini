from sqlalchemy.orm import Session

from models import User


def fake_decode_token(db: Session, token: str):
    user = db.query(User).filter(User.username == token).first()
    return user
