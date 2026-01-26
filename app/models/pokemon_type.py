from app.core.database import Base
from sqlalchemy import Column, Integer, ForeignKey, UniqueConstraint
from sqlalchemy.orm import relationship

class PokemonType(Base):
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
        "Pokemons",
        foreign_keys=[pokemon_id],
        back_populates="pokemon_types"
    )
    type = relationship(
        "Types",
        foreign_keys=[type_id],
        back_populates="pokemon_types"
    )
