""" Initial alembic for creating table structure

Revision ID: be4dfe28322a
Revises: 
Create Date: 2025-12-11 11:19:20.445415

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa

# revision identifiers, used by Alembic.
revision: str = 'be4dfe28322a'
down_revision: Union[str, Sequence[str], None] = None
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    """Upgrade schema."""
    op.create_table(
        "types",
        sa.Column("id", sa.Integer, primary_key=True),
        sa.Column("name", sa.String, unique=True, index=True),
    )

    op.create_table(
        "pokemons",
        sa.Column("id", sa.Integer, primary_key=True, index=True),
        sa.Column("name", sa.String, unique=True, index=True),
        sa.Column("height", sa.Integer),
        sa.Column("weight", sa.Integer),
        sa.Column("description", sa.String),
        # No category here since this is base migration
    )

    op.create_table(
        "pokemon_types",
        sa.Column("pokemon_id", sa.Integer, sa.ForeignKey("pokemons.id"), primary_key=True),
        sa.Column("type_id", sa.Integer, sa.ForeignKey("types.id"), primary_key=True),
    )


def downgrade() -> None:
    """Downgrade schema."""
    op.drop_table("pokemon_types")
    op.drop_table("pokemons")
    op.drop_table("types")
