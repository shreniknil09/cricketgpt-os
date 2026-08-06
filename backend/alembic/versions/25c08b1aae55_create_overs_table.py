"""Create overs table

Revision ID: 25c08b1aae55
Revises: 9687231b0401
Create Date: 2026-08-05 11:33:24.668012
"""

from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = "25c08b1aae55"
down_revision: Union[str, Sequence[str], None] = "9687231b0401"
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:

    op.create_table(
        "overs",

        sa.Column("id", sa.Integer(), nullable=False),
        sa.Column("innings_id", sa.Integer(), nullable=False),
        sa.Column("over_number", sa.Integer(), nullable=False),
        sa.Column("bowler_id", sa.Integer(), nullable=False),
        sa.Column("runs", sa.Integer(), nullable=False),
        sa.Column("wickets", sa.Integer(), nullable=False),
        sa.Column("status", sa.String(length=20), nullable=False),

        sa.ForeignKeyConstraint(
            ["innings_id"],
            ["innings.id"],
        ),

        sa.ForeignKeyConstraint(
            ["bowler_id"],
            ["players.id"],
        ),

        sa.PrimaryKeyConstraint("id"),
    )

    op.create_index(
        op.f("ix_overs_id"),
        "overs",
        ["id"],
        unique=False,
    )


def downgrade() -> None:

    op.drop_index(
        op.f("ix_overs_id"),
        table_name="overs",
    )

    op.drop_table("overs")