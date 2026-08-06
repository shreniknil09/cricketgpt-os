from sqlalchemy.orm import Session

from app.models.bowler_match_stats import BowlerMatchStats


def get_all_bowler_stats(db: Session):
    return db.query(BowlerMatchStats).all()


def get_bowler_stats_by_id(
    db: Session,
    stats_id: int,
):
    return (
        db.query(BowlerMatchStats)
        .filter(BowlerMatchStats.id == stats_id)
        .first()
    )


def get_match_bowler_stats(
    db: Session,
    match_id: int,
    player_id: int,
):
    return (
        db.query(BowlerMatchStats)
        .filter(
            BowlerMatchStats.match_id == match_id,
            BowlerMatchStats.player_id == player_id,
        )
        .first()
    )


def create_bowler_stats(
    db: Session,
    stats,
):
    new_stats = BowlerMatchStats(
        match_id=stats.match_id,
        player_id=stats.player_id,
    )

    db.add(new_stats)
    db.commit()
    db.refresh(new_stats)

    return new_stats