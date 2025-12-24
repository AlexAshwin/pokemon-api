from pydantic import BaseModel, Field, field_validator
from typing import List
from fastapi import Form

class PokemonBase(BaseModel):
    name: str = Field(..., min_length=3, max_length=50, example="Bulbasaur")
    type: List[str] = Field(..., example=["Grass", "Poison"])
    category: str = Field(..., min_length=3, max_length=50, example="Seed")
    height: float = Field(..., gt=0, example="0.4")
    weight: float = Field(..., gt=0, example="6")
    description: str = Field(..., min_length=10, max_length=300,
                             example="A strange seed was planted on its back at birth. "
                                     "The plant sprouts and grows with this Pokémon.")
    
class PokemonResponse(PokemonBase):
    id: int = Field(..., example=1)

    @classmethod
    def form_orm_pokemon(cls, pokemon):
        return cls(
            id=pokemon.id,
            name=pokemon.name,
            type=[t.name for t in pokemon.types],
            category=pokemon.category,
            height=pokemon.height,
            weight=pokemon.weight,
            description=pokemon.description
        )

class PokemonCreateRequest(PokemonBase):
    @classmethod
    def as_form(
        cls,
        name: str = Form(..., min_length=3, max_length=50, description="Bulbasaur"),
        type: str = Form(..., description="Grass, Poison"),
        category: str = Form(..., min_length=3, max_length=50, description="Seed"),
        height: float = Form(..., gt=0, description="0.4"),
        weight: float = Form(..., gt=0, description="6"),
        description: str = Form(..., min_length=10, max_length=300,
                             description="A strange seed was planted on its back at birth. "
                                     "The plant sprouts and grows with this Pokémon."),
    ):
        type_list = [t.strip() for t in type.split(",")]
        return cls(
            name=name,
            type=type_list,
            category=category,
            height=height,
            weight=weight,
            description=description
        )
