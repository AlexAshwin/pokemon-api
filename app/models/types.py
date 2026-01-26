from app.core.database import Base
from app.models.type_effectiveness import TypeEffectiveness
from app.models.pokemon_type import PokemonType
from sqlalchemy import Column, Integer, String
from sqlalchemy.orm import relationship
from sqlalchemy.ext.associationproxy import association_proxy


class Types(Base):
    __tablename__ = "types"
    # Column names
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, unique=True, index=True)
    # Relationship to association table
    pokemon_types = relationship("PokemonType",
                                 foreign_keys=[PokemonType.type_id],
                                 back_populates="type",
                                 order_by= lambda: PokemonType.slot,
                                 cascade="all, delete-orphan")
    attacks = relationship(
        "TypeEffectiveness",
        foreign_keys=[TypeEffectiveness.attacking_type_id],
        back_populates="attacking_type",
        cascade="all, delete-orphan",
    )
    defenses = relationship(
        "TypeEffectiveness",
        foreign_keys=[TypeEffectiveness.defending_type_id],
        back_populates="defending_type",
        cascade="all, delete-orphan",
    )
    # Optional: direct access to pokemons
    pokemons = association_proxy("pokemon_types", "pokemon")
    attacked_types = association_proxy("attacks","defending_type")
    defending_type = association_proxy("defenses","attacking_type")