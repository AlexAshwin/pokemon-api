from core.database import Base
from sqlalchemy import Column, Integer, String
from sqlalchemy.orm import relationship
from sqlalchemy.ext.associationproxy import association_proxy

from models.pokemon_type import PokemonType

class Pokemons(Base):
    __tablename__ = "pokemons"
    # Column names
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, unique=True, index=True)
    height = Column(Integer)
    weight = Column(Integer)
    category = Column(String)
    description = Column(String)
    # Relationship to association table
    pokemon_types = relationship(
        "PokemonType",
        back_populates="pokemon",
        order_by=lambda: PokemonType.slot,
        cascade="all, delete-orphan"
    )
    # Optional: direct access to types
    types = association_proxy("pokemon_types", "type")