import uuid

from fastapi import HTTPException, status
from sqlalchemy.orm import Session

from models import Team
from schemas import team_schemas


async def get_all_teams(db: Session):
    teams = db.query(Team).all()
    return teams


async def get_team_by_id(db: Session, team_id: str):
    team = db.query(Team).filter(Team.id == team_id).first()
    if not team:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail='No team with this ID')
    return team


async def create_team(db: Session, user_id: str, team: team_schemas.TeamCreate):
    new_team = Team(**team.dict(), owner_id=user_id, id=str(uuid.uuid4()))
    db.add(new_team)
    db.commit()
    db.refresh(new_team)
    return new_team


async def update_team(db: Session, team_id: str, team: team_schemas.TeamCreate):
    current_team = db.query(Team).filter(Team.id == team_id).first()
    current_team.name = team.name
    db.add(current_team)
    db.commit()
    db.refresh(current_team)
    return current_team


async def delete_team(db: Session, team_id: str):
    team = db.query(Team).filter(Team.id == team_id).first()
    db.delete(team)
    db.commit()
    return team
