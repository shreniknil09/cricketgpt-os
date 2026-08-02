from sqlalchemy import Boolean, ForeignKey, Integer
from sqlalchemy.orm import Mapped, mapped_column

from app.database.base import Base


class PlayingXI(Base):
    __tablename__ = "playing_xi"

    id: Mapped[int] = mapped_column(
        Integer,
        primary_key=True,
        index=True,
    )

    match_id: Mapped[int] = mapped_column(
        ForeignKey("matches.id"),
        nullable=False,
    )

    team_id: Mapped[int] = mapped_column(
        ForeignKey("teams.id"),
        nullable=False,
    )

    player_id: Mapped[int] = mapped_column(
        ForeignKey("players.id"),
        nullable=False,
    )

    batting_position: Mapped[int] = mapped_column(
        Integer,
        nullable=False,
    )

    is_captain: Mapped[bool] = mapped_column(
        Boolean,
        default=False,
    )

    is_wicketkeeper: Mapped[bool] = mapped_column(
        Boolean,
        default=False,
    )