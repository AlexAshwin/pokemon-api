from fastapi import HTTPException,status

from app.models.types import Types
from app.models.pokemons import Pokemons
from app.models.pokemon_type import PokemonType
from app.services.BaseServices import BaseService

class PokemonService(BaseService):
    def __init__(self, db):
        super().__init__(db)

    def get_pokemon_by_id(self, pokemon_id: int):
        return self.get_single_obj(Pokemons, "id", pokemon_id)

    def get_pokemon_by_name(self, pokemon_name: str):
        return self.get_single_obj(Pokemons, "name", pokemon_name)

    def get_pokemons_by_type(self, type_name: str):
        type_obj = self.get_single_obj(Types, "name", type_name)
        return type_obj.pokemons

    # Helper function to assign types to a pokemon
    def assign_types_to_pokemon(self,pokemon_obj, type_names: list[str]):
        if len(type_names) > 2:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="A pokemon can have at most 2 types")
        if len(type_names) != len(set(type_names)):
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Duplicate types are not allowed"
            )
        types = self.get_multiple_objs(Types, "name", set(type_names))
        for index, type_name in enumerate(types):
            pokemon_type_obj = PokemonType(
                pokemon_id=pokemon_obj.id,
                type_id=type_name.id,
                slot=index + 1
            )
            self.db.add(pokemon_type_obj)
