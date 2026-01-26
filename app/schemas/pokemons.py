from pydantic import BaseModel, Field
from typing import Optional, Dict, List
from fastapi import Form, HTTPException
import re


class PokemonBase(BaseModel):
    name: str = Field(..., min_length=3, max_length=50, examples=["Bulbasaur"])
    types: List[str] = Field(..., examples=["Grass", "Poison"])
    category: str = Field(..., min_length=3, max_length=50, examples=["Seed"])
    height: float = Field(..., gt=0, examples=["0.4"])
    weight: float = Field(..., gt=0, examples=["6"])
    description: str = Field(..., min_length=10, max_length=300,
                             examples=["A strange seed was planted on its back at birth. "
                                       "The plant sprouts and grows with this Pokémon."])

    @staticmethod
    def capitalize_sentences(text: str) -> str:
        text = text.strip()
        return re.sub(
            r'(^\s*[a-z])|([.!?]\s+[a-z])',
            lambda m: m.group().upper(),
            text
        )


class PokemonResponse(PokemonBase):
    id: int = Field(..., examples=[1])

    @classmethod
    def form_orm_pokemon(cls, pokemon):
        return cls(
            id=pokemon.id,
            name=pokemon.name,
            types=[t.type.name for t in sorted(pokemon.pokemon_types, key=lambda x: x.slot)],
            category=pokemon.category,
            height=pokemon.height,
            weight=pokemon.weight,
            description=pokemon.description
        )


class PokemonCreateRequest(PokemonBase):
    types: Dict[str,int]
    @classmethod
    def as_form(
            cls,
            name: str = Form(..., min_length=3, max_length=50, description="Name of Pokemon", examples=["Bulbasaur"]),
            types: str = Form(..., description="Pokemon Type", examples=["Grass, Poison"]),
            category: str = Form(..., min_length=3, max_length=50, description="Category of Pokemon",
                                 examples=["Seed"]),
            height: float = Form(..., gt=0, description="Height of Pokemon in meters", examples=["4"]),
            weight: float = Form(..., gt=0, description="Weight of Pokemon in kg", examples=[6]),
            description: str = Form(..., min_length=10, max_length=300,
                                    description="Short information about the Pokemon",
                                    examples=["A strange seed was planted on its back at birth. "
                                              "The plant sprouts and grows with this Pokémon."]),
    ):
        def convert_to_dict(types_str: str) -> Dict[str, int]:
            type_list = [t.strip().capitalize() for t in types_str.split(",")]
            if len(type_list) != len(set(type_list)):
                raise HTTPException(
                    status_code=400,
                    detail="Duplicate Pokémon types are not allowed"
            )
            return {t: index + 1 for index, t in enumerate(type_list)}
        return cls(
            name=name.capitalize(),
            types=convert_to_dict(types_str=types),
            category=category.capitalize(),
            height=height,
            weight=weight,
            description=cls.capitalize_sentences(description)
        )


class PokemonUpdateRequest(PokemonBase):
    name: Optional[str] = Field(None, min_length=3, max_length=50)
    types: Optional[Dict[str,int]] = None
    category: Optional[str] = Field(None, min_length=3, max_length=50)
    height: Optional[float] = Field(None, gt=0)
    weight: Optional[float] = Field(None, gt=0)
    description: Optional[str] = Field(None, min_length=10, max_length=300)

    @classmethod
    def as_form(
            cls,
            name: Optional[str] = Form(None, min_length=3, max_length=50),
            types: Optional[str] = Form(None),
            category: Optional[str] = Form(None, min_length=3, max_length=50),
            height: Optional[float] = Form(None, gt=0, ),
            weight: Optional[float] = Form(None, gt=0, ),
            description: Optional[str] = Form(None, min_length=10, max_length=300, ),
    ):
        data = {}
        if name is not None:
            data["name"] = name.capitalize()
        if types is not None:
            type_list = [t.strip().capitalize() for t in types.split(",")]
            if len(type_list) != len(set(type_list)):
                raise HTTPException(
                    status_code=400,
                    detail="Duplicate Pokémon types are not allowed"
                )
            data["types"] = {t: index + 1 for index, t in enumerate(type_list)}
        if category is not None:
            data["category"] = category.capitalize()
        if height is not None:
            data["height"] = height
        if weight is not None:
            data["weight"] = weight
        if description is not None:
            data["description"] = cls.capitalize_sentences(description)
        return cls(**data)
