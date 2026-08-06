from sqlalchemy import (
    Boolean,
    Float,
    ForeignKey,
    Integer,
    String,
)

from sqlalchemy.orm import (
    Mapped,
    mapped_column,
)

from app.database.base import Base


class PlayerMatchStats(Base):
    __tablename__ = "player_match_stats"

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

    runs: Mapped[int] = mapped_column(
        Integer,
        default=0,
    )

    balls: Mapped[int] = mapped_column(
        Integer,
        default=0,
    )

    fours: Mapped[int] = mapped_column(
        Integer,
        default=0,
    )

    sixes: Mapped[int] = mapped_column(
        Integer,
        default=0,
    )

    strike_rate: Mapped[float] = mapped_column(
        Float,
        default=0.0,
    )

    is_out: Mapped[bool] = mapped_column(
        Boolean,
        default=False,
    )

    dismissal_type: Mapped[str | None] = mapped_column(
        String(30),
        nullable=True,
    )