from app.schemas.pokemons import PokemonResponse
from app.core.dependencies import pokemon_service_dependency
from app.models.pokemons import Pokemons
from app.models.pokemon_type import PokemonType
from app.models.types import Types

from fastapi import APIRouter, status
from sqlalchemy.orm import selectinload

router = APIRouter(
    prefix="/pokemons",
    tags=["pokemons"]
)


# ---------------------------
# GET endpoints
# ---------------------------

# Endpoint to get all Pokemons
@router.get("/", response_model=list[PokemonResponse], status_code=status.HTTP_200_OK)
async def get_all_pokemons(service: pokemon_service_dependency):
    pokemons_list = service.get_all_pokemons(
        relations=[selectinload(Pokemons.pokemon_types).selectinload(PokemonType.type)])
    return [PokemonResponse.form_orm_pokemon(p) for p in pokemons_list]


# Endpoint to get a Pokemon by id
@router.get("/{id}", response_model=PokemonResponse, status_code=status.HTTP_200_OK)
async def get_pokemon_by_id(id: int, service: pokemon_service_dependency):
    pokemon_obj = service.get_pokemon_by_id(pokemon_id=id, relations=[
        selectinload(Pokemons.pokemon_types).selectinload(PokemonType.type)])
    return PokemonResponse.form_orm_pokemon(pokemon_obj)


# Endpoint to get a Pokemon by name
@router.get("/name/{name}", response_model=PokemonResponse, status_code=status.HTTP_200_OK)
async def get_pokemon_by_name(name: str, service: pokemon_service_dependency):
    pokemon_obj = service.get_pokemon_by_name(pokemon_name=name.capitalize(), relations=[
        selectinload(Pokemons.pokemon_types).selectinload(PokemonType.type)])
    return PokemonResponse.form_orm_pokemon(pokemon_obj)


# Endpoint to get Pokemons by type
@router.get("/type/{type_name}", response_model=list[PokemonResponse], status_code=status.HTTP_200_OK)
async def get_pokemons_by_type(type_name: str, service: pokemon_service_dependency):
    pokemons_list = service.get_pokemons_by_type(type_name=type_name.capitalize(),
                                                 relations=[selectinload(Types.pokemon_types).selectinload(
                                                     PokemonType.pokemon).selectinload(
                                                     Pokemons.pokemon_types).selectinload(
                                                     PokemonType.type)])
    return [PokemonResponse.form_orm_pokemon(p) for p in pokemons_list]
