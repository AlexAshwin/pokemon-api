from models.pokemons import Pokemons
from models.types import Types
from schemas.pokemons import PokemonResponse
from core.dependencies import db_dependency

from fastapi import APIRouter, HTTPException, status

router = APIRouter(
    prefix="/pokemons",
    tags=["pokemons"]
)

# ---------------------------
# GET endpoints
# ---------------------------

# Endpoint to get all Pokemons
@router.get("/", response_model=list[PokemonResponse], status_code=status.HTTP_200_OK)
async def get_all_pokemons(db: db_dependency):
    pokemons_list = db.query(Pokemons).all()
    return [PokemonResponse.form_orm_pokemon(p) for p in pokemons_list]

# Endpoint to get a Pokemon by id
@router.get("/{id}", response_model=PokemonResponse, status_code=status.HTTP_200_OK)
async def get_pokemon_by_id(id: int, db: db_dependency):
    pokemon_obj =  db.query(Pokemons).filter(Pokemons.id == id).first()
    if not pokemon_obj:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Pokemon id not found")
    return PokemonResponse.form_orm_pokemon(pokemon_obj)

# Endpoint to get a Pokemon by name
@router.get("/name/{name}", response_model=PokemonResponse, status_code=status.HTTP_200_OK)
async def get_pokemon_by_name(name: str, db: db_dependency):
    pokemon_obj = db.query(Pokemons).filter(Pokemons.name == name).first()
    if not pokemon_obj:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Pokemon name not found")
    return PokemonResponse.form_orm_pokemon(pokemon_obj)

# Endpoint to get Pokemons by type
@router.get("/type/{type_name}", response_model=list[PokemonResponse], status_code=status.HTTP_200_OK)
async def get_pokemons_by_type(type_name: str, db: db_dependency):
    type_obj = db.query(Types).filter(Types.name == type_name).first()
    if not type_obj:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Type not found")
    pokemons_list = type_obj.pokemons
    return [PokemonResponse.form_orm_pokemon(p) for p in pokemons_list]
