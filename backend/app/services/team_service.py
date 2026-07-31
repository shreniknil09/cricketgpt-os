from sqlalchemy.orm import Session

from app.models.team import Team


def get_all_teams(db: Session):
    return db.query(Team).all()


def create_team(db: Session, team):
    new_team = Team(
        name=team.name,
        short_name=team.short_name,
        country=team.country,
    )

    db.add(new_team)
    db.commit()
    db.refresh(new_team)

    return new_team


def get_team_by_id(db: Session, team_id: int):
    return db.query(Team).filter(Team.id == team_id).first()


def update_team(db: Session, team_id: int, updated_team):
    team = db.query(Team).filter(Team.id == team_id).first()

    if not team:
        return None

    team.name = updated_team.name
    team.short_name = updated_team.short_name
    team.country = updated_team.country

    db.commit()
    db.refresh(team)

    return team


def delete_team(db: Session, team_id: int):
    team = db.query(Team).filter(Team.id == team_id).first()

    if not team:
        return None

    db.delete(team)
    db.commit()

    return team