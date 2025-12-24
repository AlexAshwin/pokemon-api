from app.core.database import Base
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
                                 back_populates="type",
                                 cascade="all, delete-orphan")
    # Optional: direct access to pokemons
    pokemons = association_proxy("pokemon_types", "pokemon")