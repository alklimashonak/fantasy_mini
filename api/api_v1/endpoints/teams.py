from typing import List

from fastapi import APIRouter, Depends, status
from sqlalchemy.orm import Session

from crud import team_crud
from api import dependencies
from schemas import team_schemas


router = APIRouter()


@router.get('/', response_model=List[team_schemas.TeamDB])
async def read_all_teams(db: Session = Depends(dependencies.get_db)):
    teams = team_crud.get_all_teams(db=db)
    return teams


@router.get('/{team_id}', response_model=team_schemas.TeamDBFull)
async def read_team(team_id: int, db: Session = Depends(dependencies.get_db)):
    team = team_crud.get_team_by_id(db=db, team_id=team_id)
    return team


@router.post('/', status_code=status.HTTP_201_CREATED, response_model=team_schemas.TeamDB)
async def create_team(user_id: str, team: team_schemas.TeamCreate, db: Session = Depends(dependencies.get_db)):
    new_team = team_crud.create_team(db=db, user_id=user_id, team=team)
    return new_team


@router.put('/{team_id}', status_code=status.HTTP_200_OK, response_model=team_schemas.TeamDB)
async def update_team(team_id: int, team: team_schemas.TeamCreate, db: Session = Depends(dependencies.get_db)):
    updated_team = team_crud.update_team(db=db, team_id=team_id, team=team)
    return updated_team
