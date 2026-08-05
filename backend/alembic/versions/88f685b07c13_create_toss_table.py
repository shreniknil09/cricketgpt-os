"""Create Toss table

Revision ID: 88f685b07c13
Revises: 5046dc072181
Create Date: 2026-08-04 23:05:11.456639
"""

from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = "88f685b07c13"
down_revision: Union[str, Sequence[str], None] = "5046dc072181"
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:

    op.create_table(
        "tosses",

        sa.Column(
            "id",
            sa.Integer(),
            primary_key=True,
            index=True,
        ),

        sa.Column(
            "match_id",
            sa.Integer(),
            sa.ForeignKey("matches.id"),
            nullable=False,
            unique=True,
        ),

        sa.Column(
            "winning_team_id",
            sa.Integer(),
            sa.ForeignKey("teams.id"),
            nullable=False,
        ),

        sa.Column(
            "decision",
            sa.String(length=10),
            nullable=False,
        ),

        sa.Column(
            "batting_team_id",
            sa.Integer(),
            sa.ForeignKey("teams.id"),
            nullable=False,
        ),

        sa.Column(
            "bowling_team_id",
            sa.Integer(),
            sa.ForeignKey("teams.id"),
            nullable=False,
        ),
    )


def downgrade() -> None:
    op.drop_table("tosses")