from fastapi import HTTPException, status
from sqlalchemy.orm import Session

from models import Team
from schemas import team_schemas


def get_all_teams(db: Session):
    teams = db.query(Team).all()
    return teams


def get_team_by_id(db: Session, team_id: int):
    team = db.query(Team).filter(Team.id == team_id).first()
    if not team:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail='No team with this ID')
    return team


def create_team(db: Session, user_id: str, team: team_schemas.TeamCreate):
    new_team = Team(**team.dict(), owner_id=user_id)
    db.add(new_team)
    db.commit()
    db.refresh(new_team)
    return new_team


def update_team(db: Session, team_id: int, team: team_schemas.TeamCreate):
    current_team = db.query(Team).filter(Team.id == team_id).first()
    current_team.name = team.name
    db.add(current_team)
    db.commit()
    db.refresh(current_team)
    return current_team
