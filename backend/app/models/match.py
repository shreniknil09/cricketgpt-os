from datetime import date, time

from sqlalchemy import Date, ForeignKey, Integer, String, Time
from sqlalchemy.orm import Mapped, mapped_column

from app.database.base import Base


class Match(Base):
    __tablename__ = "matches"

    id: Mapped[int] = mapped_column(
        Integer,
        primary_key=True,
        index=True,
    )

    tournament_id: Mapped[int] = mapped_column(
        ForeignKey("tournaments.id"),
        nullable=False,
    )

    venue_id: Mapped[int] = mapped_column(
        ForeignKey("venues.id"),
        nullable=False,
    )

    team1_id: Mapped[int] = mapped_column(
        ForeignKey("teams.id"),
        nullable=False,
    )

    team2_id: Mapped[int] = mapped_column(
        ForeignKey("teams.id"),
        nullable=False,
    )

    match_date: Mapped[date] = mapped_column(
        Date,
        nullable=False,
    )

    match_time: Mapped[time] = mapped_column(
        Time,
        nullable=False,
    )

    status: Mapped[str] = mapped_column(
        String(30),
        default="Scheduled",
    )

    toss_winner_id: Mapped[int | None] = mapped_column(
        ForeignKey("teams.id"),
        nullable=True,
    )

    toss_decision: Mapped[str | None] = mapped_column(
        String(20),
        nullable=True,
    )

    winner_id: Mapped[int | None] = mapped_column(
        ForeignKey("teams.id"),
        nullable=True,
    )