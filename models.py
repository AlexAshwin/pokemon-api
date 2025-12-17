from database import Base
from sqlalchemy import Column, Integer, String, ForeignKey, UniqueConstraint
from sqlalchemy.orm import relationship
from sqlalchemy.ext.associationproxy import association_proxy


class types(Base):
    __tablename__ = "types"
    # Column names
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, unique=True, index=True)
    # Relationship to association table
    pokemon_types = relationship("pokemon_type",
                                 back_populates="type",
                                 cascade="all, delete-orphan")
    # Optional: direct access to pokemons
    pokemons = association_proxy("pokemon_types", "pokemon")

class pokemons(Base):
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
        "pokemon_type",
        back_populates="pokemon",
        order_by="pokemon_type.slot",
        cascade="all, delete-orphan"
    )
    # Optional: direct access to types
    types = association_proxy("pokemon_types", "type")

class pokemon_type(Base):
    __tablename__ = "pokemon_types"
    # Column names
    pokemon_id = Column(Integer, ForeignKey("pokemons.id"), primary_key=True, index=True)
    type_id = Column(Integer, ForeignKey("types.id"), primary_key=True, index=True)
    slot = Column(Integer, nullable=False)
    # Ensure slot is unique per Pokémon (important!)
    __table_args__ = (
        UniqueConstraint("pokemon_id", "slot", name="uq_pokemon_slot"),
    )
    pokemon = relationship(
        "pokemons",
        back_populates="pokemon_types"
    )
    type = relationship(
        "types",
        back_populates="pokemon_types"
    )
