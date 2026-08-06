from sqlalchemy.orm import Session

from app.models.player_match_stats import PlayerMatchStats


def get_all_player_stats(db: Session):
    return db.query(PlayerMatchStats).all()


def get_player_stats_by_id(
    db: Session,
    stats_id: int,
):
    return (
        db.query(PlayerMatchStats)
        .filter(PlayerMatchStats.id == stats_id)
        .first()
    )


def get_match_player_stats(
    db: Session,
    match_id: int,
    player_id: int,
):
    return (
        db.query(PlayerMatchStats)
        .filter(
            PlayerMatchStats.match_id == match_id,
            PlayerMatchStats.player_id == player_id,
        )
        .first()
    )


def create_player_stats(
    db: Session,
    stats,
):
    new_stats = PlayerMatchStats(
        match_id=stats.match_id,
        player_id=stats.player_id,
    )

    db.add(new_stats)
    db.commit()
    db.refresh(new_stats)

    return new_stats