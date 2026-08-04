from logging.config import fileConfig

from sqlalchemy import engine_from_config
from sqlalchemy import pool

from alembic import context

from app.database.base import Base

# Import all models so Alembic can detect them
from app.models.user import User
from app.models.team import Team
from app.models.player import Player
from app.models.venue import Venue
from app.models.tournament import Tournament
from app.models.match import Match
from app.models.playing_xi import PlayingXI
from app.models.toss import Toss

# this is the Alembic Config object, which provides
# access to the values within the .ini file in use.
config = context.config

# Interpret the config file for Python logging.
if config.config_file_name is not None:
    fileConfig(config.config_file_name)

# SQLAlchemy metadata
target_metadata = Base.metadata