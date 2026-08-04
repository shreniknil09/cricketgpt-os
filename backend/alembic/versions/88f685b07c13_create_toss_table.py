"""Create Toss table

Revision ID: 88f685b07c13
Revises: 5046dc072181
Create Date: 2026-08-04 23:05:11.456639

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '88f685b07c13'
down_revision: Union[str, Sequence[str], None] = '5046dc072181'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    """Upgrade schema."""
    pass


def downgrade() -> None:
    """Downgrade schema."""
    pass
