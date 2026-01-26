"""Adding slots in pokemon_types table

Revision ID: d8a8b29efedf
Revises: 7febf4efd0cb
Create Date: 2025-12-14 22:35:55.180809

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = 'd8a8b29efedf'
down_revision: Union[str, Sequence[str], None] = '7febf4efd0cb'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    """Upgrade schema."""
    op.add_column("pokemon_types", sa.Column("slot", sa.Integer, nullable=True))


def downgrade() -> None:
    """Downgrade schema."""
    op.drop_column('pokemon_types', 'slot')
