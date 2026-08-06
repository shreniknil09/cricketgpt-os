"""Create balls table

Revision ID: 5aac78955112
Revises: 25c08b1aae55
Create Date: 2026-08-05 11:45:20.753944
"""

from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


revision: str = "5aac78955112"
down_revision: Union[str, Sequence[str], None] = "25c08b1aae55"
branch_labels = None
depends_on = None


def upgrade() -> None:

    op.create_table(
        "balls",

        sa.Column("id", sa.Integer(), nullable=False),
        sa.Column("over_id", sa.Integer(), nullable=False),
        sa.Column("ball_number", sa.Integer(), nullable=False),
        sa.Column("striker_id", sa.Integer(), nullable=False),
        sa.Column("non_striker_id", sa.Integer(), nullable=False),
        sa.Column("bowler_id", sa.Integer(), nullable=False),
        sa.Column("runs", sa.Integer(), nullable=False),
        sa.Column("extra_type", sa.String(length=20), nullable=True),
        sa.Column("extra_runs", sa.Integer(), nullable=False),
        sa.Column("is_wicket", sa.Boolean(), nullable=False),
        sa.Column("dismissal_type", sa.String(length=30), nullable=True),
        sa.Column("commentary", sa.String(length=255), nullable=True),

        sa.ForeignKeyConstraint(
            ["over_id"],
            ["overs.id"],
        ),

        sa.ForeignKeyConstraint(
            ["striker_id"],
            ["players.id"],
        ),

        sa.ForeignKeyConstraint(
            ["non_striker_id"],
            ["players.id"],
        ),

        sa.ForeignKeyConstraint(
            ["bowler_id"],
            ["players.id"],
        ),

        sa.PrimaryKeyConstraint("id"),
    )

    op.create_index(
        op.f("ix_balls_id"),
        "balls",
        ["id"],
        unique=False,
    )


def downgrade() -> None:

    op.drop_index(
        op.f("ix_balls_id"),
        table_name="balls",
    )

    op.drop_table("balls")