from sqlalchemy import (
    ForeignKey,
    Integer,
    String,
)
from sqlalchemy.orm import (
    Mapped,
    mapped_column,
)

from app.database.base import Base


class Innings(Base):
    __tablename__ = "innings"

    id: Mapped[int] = mapped_column(
        Integer,
        primary_key=True,
        index=True,
    )

    match_id: Mapped[int] = mapped_column(
        ForeignKey("matches.id"),
        nullable=False,
    )

    innings_number: Mapped[int] = mapped_column(
        Integer,
        nullable=False,
    )

    batting_team_id: Mapped[int] = mapped_column(
        ForeignKey("teams.id"),
        nullable=False,
    )

    bowling_team_id: Mapped[int] = mapped_column(
        ForeignKey("teams.id"),
        nullable=False,
    )

    # -------------------------
    # Current Match State
    # -------------------------

    current_striker_id: Mapped[int | None] = mapped_column(
        ForeignKey("players.id"),
        nullable=True,
    )

    current_non_striker_id: Mapped[int | None] = mapped_column(
        ForeignKey("players.id"),
        nullable=True,
    )

    current_bowler_id: Mapped[int | None] = mapped_column(
        ForeignKey("players.id"),
        nullable=True,
    )

    # -------------------------
    # Score
    # -------------------------

    runs: Mapped[int] = mapped_column(
        Integer,
        default=0,
    )

    wickets: Mapped[int] = mapped_column(
        Integer,
        default=0,
    )

    overs: Mapped[int] = mapped_column(
        Integer,
        default=0,
    )

    balls: Mapped[int] = mapped_column(
        Integer,
        default=0,
    )

    status: Mapped[str] = mapped_column(
        String(20),
        default="Not Started",
    )