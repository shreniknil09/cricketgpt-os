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


class Over(Base):
    __tablename__ = "overs"

    id: Mapped[int] = mapped_column(
        Integer,
        primary_key=True,
        index=True,
    )

    innings_id: Mapped[int] = mapped_column(
        ForeignKey("innings.id"),
        nullable=False,
    )

    over_number: Mapped[int] = mapped_column(
        Integer,
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

    wickets: Mapped[int] = mapped_column(
        Integer,
        default=0,
    )

    status: Mapped[str] = mapped_column(
        String(20),
        default="Not Started",
    )