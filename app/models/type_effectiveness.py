from sqlalchemy import Column, ForeignKey, Integer, UniqueConstraint
from sqlalchemy.orm import relationship

from app.core.database import Base

class TypeEffectiveness(Base):
    __tablename__ = "type_effectiveness"
    # Column names
    attacking_type_id = Column(Integer, ForeignKey("types.id"),primary_key=True, nullable=False, index=True)
    defending_type_id = Column(Integer, ForeignKey("types.id"),primary_key=True, nullable=False, index=True)
    effectiveness_multiplier = Column(Integer, nullable=False)
    # Ensure unique effectiveness per type combination
    __table_args__ = (
        UniqueConstraint("attacking_type_id", "defending_type_id", name="uq_type_effectiveness"),
    )
    # Relationships
    attacking_type = relationship(
        "Types",
        foreign_keys=[attacking_type_id],
        back_populates="attacks",
    )
    defending_type = relationship(
        "Types",
        foreign_keys=[defending_type_id],
        back_populates="defenses",
    )




