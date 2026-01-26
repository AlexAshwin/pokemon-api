from fastapi import HTTPException, status
from sqlalchemy.orm import selectinload
from typing import Dict

from app.models.types import Types
from app.models.pokemons import Pokemons
from app.models.pokemon_type import PokemonType
from app.services.BaseServices import BaseService


class PokemonService(BaseService):
    def __init__(self, db):
        super().__init__(db)

    def get_all_pokemons(self, relations=None):
        # Pokemons -> PokemonType -> Type
        return self.get_all_obj(model=Pokemons,
                                relations=relations)

    def get_pokemon_by_id(self, pokemon_id: int, relations=None):
        # Pokemons -> PokemonType -> Type
        return self.get_single_obj(model=Pokemons, attribute_name="id", attribute_value=pokemon_id,
                                   relations=relations)

    def get_pokemon_by_name(self, pokemon_name: str, relations=None):
        return self.get_single_obj(model=Pokemons, attribute_name="name", attribute_value=pokemon_name, ilike=True,
                                   relations=relations)

    def get_pokemons_by_type(self, type_name: str, relations=None):
        # Type -> PokemonType -> Pokemon -> PokemonType -> Type
        type_obj = self.get_single_obj(model=Types, attribute_name="name", attribute_value=type_name,
                                       ilike=True,
                                       relations=relations)
        return type_obj.pokemons

    def check_if_pokemon_exists(self, name: str) -> bool:
        return self.exists_by(Pokemons, "name", name)

    def delete_pokemon(self, pokemon_obj):
        try:
            self.db.delete(pokemon_obj)
            self.db.commit()
        except Exception as e:
            self.db.rollback()
            raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                                detail=f"Exception while deleting pokemon due to {e}")

    def create_pokemon(self, pokemon_request):
        try:
            new_pokemon = Pokemons(
                name=pokemon_request.name,
                height=pokemon_request.height,
                weight=pokemon_request.weight,
                category=pokemon_request.category,
                description=pokemon_request.description,
            )
            self.db.add(new_pokemon)
            self.db.flush()
            self.assign_types_to_pokemon(new_pokemon, pokemon_request.types)
            self.db.commit()
            return self.get_pokemon_by_name(pokemon_name=pokemon_request.name,
                                          relations=[selectinload(Pokemons.pokemon_types).selectinload(
                                              PokemonType.type)])
        except HTTPException:
            self.db.rollback()
            raise
        except Exception as e:
            self.db.rollback()
            raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                                detail=f"Exception while adding pokemon due to {e}")

    # Helper function to assign types to a pokemon
    def assign_types_to_pokemon(self, pokemon_obj, type_slots: Dict[str, int]):
        if not 1 <= len(type_slots) <= 2:
            raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Pokemon must have 1 or 2 types")
        types = self.get_multiple_objs(model=Types, attribute_name="name", attribute_values=type_slots.keys())
        type_map = {t.name: t for t in types}
        for name, slot in type_slots.items():
            self.db.add(
                PokemonType(
                    pokemon_id=pokemon_obj.id,
                    type_id=type_map[name].id,
                    slot=slot
                )
            )

    def update_pokemon(self, id, pokemon_request):
        try:
            pokemon = self.get_pokemon_by_id(pokemon_id=id, relations=[
                selectinload(Pokemons.pokemon_types)])
            update_data = pokemon_request.model_dump(exclude_unset=True)
            types = update_data.pop("types", None)
            for field, value in update_data.items():
                setattr(pokemon, field, value)
            if types is not None:
                pokemon_types = pokemon.pokemon_types
                pokemon_types.clear()
                self.db.flush()
                self.assign_types_to_pokemon(pokemon, types)
            self.db.commit()
            return self.get_pokemon_by_id(pokemon_id=id,
                                          relations=[selectinload(Pokemons.pokemon_types).selectinload(
                                              PokemonType.type)])
        except HTTPException:
            self.db.rollback()
            raise
        except Exception as e:
            self.db.rollback()
            raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                                detail=f"Exception while updating pokemon due to {e}")
