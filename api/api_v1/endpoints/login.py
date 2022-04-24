from fastapi import APIRouter, Depends, HTTPException
from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy.orm import Session

import utils
from api import dependencies

router = APIRouter()


@router.post("/token")
async def login(db: Session = Depends(dependencies.get_db), form_data: OAuth2PasswordRequestForm = Depends()):
    user = utils.authenticate_user(db=db, username=form_data.username, password=form_data.password)
    if not user:
        raise HTTPException(status_code=401, detail="Incorrect username or password")
    return {"access_token": user.username, "token_type": "bearer"}
