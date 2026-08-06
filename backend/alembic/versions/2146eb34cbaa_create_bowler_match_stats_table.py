"""Create bowler match stats table

Revision ID: 2146eb34cbaa
Revises: 284689e40006
Create Date: 2026-08-05 12:23:44.081123
"""

from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = "2146eb34cbaa"
down_revision: Union[str, Sequence[str], None] = "284689e40006"
branch_labels = None
depends_on = None


def upgrade() -> None:

    op.create_table(
        "bowler_match_stats",

        sa.Column(
            "id",
            sa.Integer(),
            nullable=False,
        ),

        sa.Column(
            "match_id",
            sa.Integer(),
            nullable=False,
        ),

        sa.Column(
            "player_id",
            sa.Integer(),
            nullable=False,
        ),

        sa.Column(
            "overs",
            sa.Float(),
            nullable=False,
        ),

        sa.Column(
            "balls",
            sa.Integer(),
            nullable=False,
        ),

        sa.Column(
            "maidens",
            sa.Integer(),
            nullable=False,
        ),

        sa.Column(
            "runs_given",
            sa.Integer(),
            nullable=False,
        ),

        sa.Column(
            "wickets",
            sa.Integer(),
            nullable=False,
        ),

        sa.Column(
            "economy",
            sa.Float(),
            nullable=False,
        ),

        sa.ForeignKeyConstraint(
            ["match_id"],
            ["matches.id"],
        ),

        sa.ForeignKeyConstraint(
            ["player_id"],
            ["players.id"],
        ),

        sa.PrimaryKeyConstraint("id"),
    )

    op.create_index(
        op.f("ix_bowler_match_stats_id"),
        "bowler_match_stats",
        ["id"],
        unique=False,
    )


def downgrade() -> None:

    op.drop_index(
        op.f("ix_bowler_match_stats_id"),
        table_name="bowler_match_stats",
    )

    op.drop_table("bowler_match_stats")  