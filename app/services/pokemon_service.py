from fastapi import HTTPException,status

from models.types import Types
from models.pokemon_type import PokemonType


# Helper function to assign types to a pokemon
def assign_types_to_pokemon(pokemon_obj, type_names, db):
    if len(type_names) > 2:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="A pokemon can have at most 2 types")
    for index, type_name in enumerate(type_names):
        type_obj = db.query(Types).filter(Types.name == type_name).first()
        if not type_obj:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"Type '{type_name}' not found")
        pokemon_type_obj = PokemonType(pokemon_id=pokemon_obj.id, type_id=type_obj.id, slot=index + 1)
        db.add(pokemon_type_obj)
