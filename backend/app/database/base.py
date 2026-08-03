from sqlalchemy.orm import DeclarativeBase


class Base(DeclarativeBase):
    pass


# Import every model so SQLAlchemy registers relationships
from app.models import *