"""Create innings table

Revision ID: 9687231b0401
Revises: 88f685b07c13
Create Date: 2026-08-05 10:37:05.956544
"""

from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


revision: str = "9687231b0401"
down_revision: Union[str, Sequence[str], None] = "88f685b07c13"
branch_labels = None
depends_on = None


def upgrade() -> None:

    op.create_table(
        "innings",

        sa.Column(
            "id",
            sa.Integer(),
            primary_key=True,
        ),

        sa.Column(
            "match_id",
            sa.Integer(),
            sa.ForeignKey("matches.id"),
            nullable=False,
        ),

        sa.Column(
            "innings_number",
            sa.Integer(),
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

        sa.Column(
            "runs",
            sa.Integer(),
            nullable=False,
            server_default="0",
        ),

        sa.Column(
            "wickets",
            sa.Integer(),
            nullable=False,
            server_default="0",
        ),

        sa.Column(
            "overs",
            sa.Integer(),
            nullable=False,
            server_default="0",
        ),

        sa.Column(
            "balls",
            sa.Integer(),
            nullable=False,
            server_default="0",
        ),

        sa.Column(
            "status",
            sa.String(length=20),
            nullable=False,
            server_default="Not Started",
        ),
    )


def downgrade() -> None:
    op.drop_table("innings")