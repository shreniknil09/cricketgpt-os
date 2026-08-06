from sqlalchemy import (
    Float,
    ForeignKey,
    Integer,
)
from sqlalchemy.orm import (
    Mapped,
    mapped_column,
)

from app.database.base import Base


class BowlerMatchStats(Base):
    __tablename__ = "bowler_match_stats"

    id: Mapped[int] = mapped_column(
        Integer,
        primary_key=True,
        index=True,
    )

    match_id: Mapped[int] = mapped_column(
        ForeignKey("matches.id"),
        nullable=False,
    )

    player_id: Mapped[int] = mapped_column(
        ForeignKey("players.id"),
        nullable=False,
    )

    overs: Mapped[float] = mapped_column(
        Float,
        default=0.0,
    )

    balls: Mapped[int] = mapped_column(
        Integer,
        default=0,
    )

    maidens: Mapped[int] = mapped_column(
        Integer,
        default=0,
    )

    runs_given: Mapped[int] = mapped_column(
        Integer,
        default=0,
    )

    wickets: Mapped[int] = mapped_column(
        Integer,
        default=0,
    )

    economy: Mapped[float] = mapped_column(
        Float,
        default=0.0,
    )