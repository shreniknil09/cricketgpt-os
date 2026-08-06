"""Create player match stats table

Revision ID: 284689e40006
Revises: 5aac78955112
Create Date: 2026-08-05 12:05:30.903220
"""

from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


revision = "284689e40006"
down_revision = "5aac78955112"
branch_labels = None
depends_on = None


def upgrade():

    op.create_table(
        "player_match_stats",

        sa.Column("id", sa.Integer(), nullable=False),

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
            "runs",
            sa.Integer(),
            nullable=False,
        ),

        sa.Column(
            "balls",
            sa.Integer(),
            nullable=False,
        ),

        sa.Column(
            "fours",
            sa.Integer(),
            nullable=False,
        ),

        sa.Column(
            "sixes",
            sa.Integer(),
            nullable=False,
        ),

        sa.Column(
            "strike_rate",
            sa.Float(),
            nullable=False,
        ),

        sa.Column(
            "is_out",
            sa.Boolean(),
            nullable=False,
        ),

        sa.Column(
            "dismissal_type",
            sa.String(length=30),
            nullable=True,
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
        op.f("ix_player_match_stats_id"),
        "player_match_stats",
        ["id"],
        unique=False,
    )


def downgrade():

    op.drop_index(
        op.f("ix_player_match_stats_id"),
        table_name="player_match_stats",
    )

    op.drop_table("player_match_stats")