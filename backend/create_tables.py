from app.database.base import Base
from app.database.session import engine

from app.models.team import Team
from app.models.player import Player
from app.models.venue import Venue
from app.models.user import User

Base.metadata.create_all(bind=engine)

print("✅ Database tables created successfully!")