from sqlalchemy import String
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.database.base import Base


class Team(Base):
    __tablename__ = "teams"

    id: Mapped[int] = mapped_column(primary_key=True, index=True)
    name: Mapped[str] = mapped_column(String(100), unique=True, nullable=False)
    short_name: Mapped[str] = mapped_column(String(10), unique=True, nullable=False)
    country: Mapped[str] = mapped_column(String(50), nullable=False)

    players = relationship(
    "Player",
    back_populates="team",
    cascade="all, delete"
)