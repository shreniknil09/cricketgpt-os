from sqlalchemy import (
    Boolean,
    ForeignKey,
    Integer,
    String,
)
from sqlalchemy.orm import (
    Mapped,
    mapped_column,
)

from app.database.base import Base


class Ball(Base):
    __tablename__ = "balls"

    id: Mapped[int] = mapped_column(
        Integer,
        primary_key=True,
        index=True,
    )

    over_id: Mapped[int] = mapped_column(
        ForeignKey("overs.id"),
        nullable=False,
    )

    ball_number: Mapped[int] = mapped_column(
        Integer,
        nullable=False,
    )

    striker_id: Mapped[int] = mapped_column(
        ForeignKey("players.id"),
        nullable=False,
    )

    non_striker_id: Mapped[int] = mapped_column(
        ForeignKey("players.id"),
        nullable=False,
    )

    bowler_id: Mapped[int] = mapped_column(
        ForeignKey("players.id"),
        nullable=False,
    )

    runs: Mapped[int] = mapped_column(
        Integer,
        default=0,
    )

    extra_type: Mapped[str | None] = mapped_column(
        String(20),
        nullable=True,
    )

    extra_runs: Mapped[int] = mapped_column(
        Integer,
        default=0,
    )

    is_wicket: Mapped[bool] = mapped_column(
        Boolean,
        default=False,
    )

    dismissal_type: Mapped[str | None] = mapped_column(
        String(30),
        nullable=True,
    )

    commentary: Mapped[str | None] = mapped_column(
        String(255),
        nullable=True,
    )