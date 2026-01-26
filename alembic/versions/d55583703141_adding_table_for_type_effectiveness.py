"""Adding table for type effectiveness

Revision ID: d55583703141
Revises: d8a8b29efedf
Create Date: 2025-12-25 18:43:27.484381

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa
from sqlalchemy import ForeignKey

# revision identifiers, used by Alembic.
revision: str = 'd55583703141'
down_revision: Union[str, Sequence[str], None] = 'd8a8b29efedf'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    """Upgrade schema."""
    op.create_table(
        'type_effectiveness',
        sa.Column('attacking_type_id', sa.Integer,sa.ForeignKey("types.id"),primary_key=True, index=True),
        sa.Column('defending_type_id', sa.Integer, sa.ForeignKey("types.id"),primary_key=True, index=True),
        sa.Column('effectiveness_multiplier', sa.Float, nullable=False),
    )


def downgrade() -> None:
    """Downgrade schema."""
    op.drop_table("type_effectiveness")
