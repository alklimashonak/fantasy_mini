from typing import List

from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from crud import user_crud
from api import dependencies
from schemas import user_schemas


router = APIRouter()


@router.get('/', response_model=List[user_schemas.User])
async def read_all_users(db: Session = Depends(dependencies.get_db)):
    users = user_crud.get_all_users(db=db)
    return users


@router.get('/me', response_model=user_schemas.User)
async def read_current_user(current_user: user_schemas.User = Depends(dependencies.get_current_user)):
    return current_user


@router.get('/{user_id}', response_model=user_schemas.User)
async def read_user(user_id: str, db: Session = Depends(dependencies.get_db)):
    user = user_crud.get_user_by_id(db=db, user_id=user_id)
    return user


@router.post('/', response_model=user_schemas.User)
async def create_user(user: user_schemas.UserCreate, db: Session = Depends(dependencies.get_db)):
    new_user = user_crud.create_user(db=db, user=user)
    return new_user


@router.post('/admin', response_model=user_schemas.User)
async def create_superuser(user: user_schemas.UserCreate, db: Session = Depends(dependencies.get_db)):
    new_user = user_crud.create_user(db=db, user=user, is_admin=True)
    return new_user
