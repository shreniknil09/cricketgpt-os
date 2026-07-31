from app.database.base import Base
from app.database.connection import engine

from app.models.team import Team
from app.models.player import Player
from app.models.venue import Venue

Base.metadata.create_all(bind=engine)

print("✅ Database tables created successfully!")