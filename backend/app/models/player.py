from sqlalchemy import ForeignKey, String
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.database.base import Base


class Player(Base):
    __tablename__ = "players"

    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str] = mapped_column(String(100), nullable=False)
    batting_style: Mapped[str] = mapped_column(String(50))
    bowling_style: Mapped[str] = mapped_column(String(50))
    role: Mapped[str] = mapped_column(String(30))

    team_id: Mapped[int] = mapped_column(ForeignKey("teams.id"))

    team = relationship("Team")
    