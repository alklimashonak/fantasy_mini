from typing import List

from fastapi import APIRouter, Depends, status, HTTPException
from sqlalchemy.orm import Session

from crud import team_crud
from api import dependencies
from schemas import team_schemas, user_schemas

router = APIRouter()


@router.get('/', response_model=List[team_schemas.Team])
async def read_all_teams(db: Session = Depends(dependencies.get_db)):
    teams = team_crud.get_all_teams(db=db)
    return teams


@router.get('/my-teams', response_model=List[team_schemas.Team])
async def read_teams_of_current_user(current_user: user_schemas.User = Depends(dependencies.get_current_user)):
    return current_user.teams


@router.get('/{team_id}', response_model=team_schemas.Team)
async def read_team(team_id: str, db: Session = Depends(dependencies.get_db)):
    team = team_crud.get_team_by_id(db=db, team_id=team_id)
    return team


@router.post('/', status_code=status.HTTP_201_CREATED, response_model=team_schemas.Team)
async def create_team(team: team_schemas.TeamCreate,
                      current_user: user_schemas.User = Depends(dependencies.get_current_user),
                      db: Session = Depends(dependencies.get_db)):
    new_team = team_crud.create_team(db=db, user_id=current_user.id, team=team)
    return new_team


@router.put('/{team_id}', status_code=status.HTTP_200_OK, response_model=team_schemas.Team)
async def update_team(
        team_id: str,
        team: team_schemas.TeamCreate,
        current_user: user_schemas.User = Depends(dependencies.get_current_user),
        db: Session = Depends(dependencies.get_db)
):
    if team_id not in [user_team.id for user_team in current_user.teams]:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail='You can update only your own team')
    updated_team = team_crud.update_team(db=db, team_id=team_id, team=team)
    return updated_team


@router.delete('/{team_id}', status_code=status.HTTP_200_OK, response_model=team_schemas.Team)
async def delete_team(
        team_id: str,
        current_user: user_schemas.User = Depends(dependencies.get_current_user),
        db: Session = Depends(dependencies.get_db)
):
    if team_id not in [user_team.id for user_team in current_user.teams]:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail='You can delete only your own team')
    deleted_team = team_crud.delete_team(db=db, team_id=team_id)
    return deleted_team
