"""Adding category to pokemons table

Revision ID: 7febf4efd0cb
Revises: be4dfe28322a
Create Date: 2025-12-11 20:36:46.076467

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '7febf4efd0cb'
down_revision: Union[str, Sequence[str], None] = 'be4dfe28322a'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    """Upgrade schema."""
    op.add_column('pokemons', sa.Column('category', sa.String, nullable=True))

def downgrade() -> None:
    """Downgrade schema."""
    op.drop_column('pokemons', 'category')
