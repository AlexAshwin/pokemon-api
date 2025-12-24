from fastapi import APIRouter,HTTPException, status, Response

from app.core.dependencies import admin_dependency, db_dependency, pokemon_create_request_dependency
from app.models.pokemons import Pokemons
from app.schemas.pokemons import PokemonResponse
from app.services.pokemon_service import assign_types_to_pokemon

router = APIRouter(
    prefix="/pokemons",
    tags=["pokemons"]
)

# ---------------------------
# Post endpoints
# ---------------------------
#Endpoints to add pokemons
@router.post("/", response_model=PokemonResponse, status_code=status.HTTP_201_CREATED)
async def create_pokemon(pokemon_request: pokemon_create_request_dependency, db: db_dependency, user: admin_dependency):
    if user is None:
        raise HTTPException(status_code=401, detail="Unauthorized")
    existing_pokemon = db.query(Pokemons).filter(Pokemons.name == pokemon_request.name).first()
    if existing_pokemon:
        raise HTTPException(status_code=status.HTTP_409_CONFLICT, detail="Pokemon already exists")
    # Create pokemon entry
    new_pokemon = Pokemons(
        name=pokemon_request.name,
        height=pokemon_request.height,
        weight=pokemon_request.weight,
        category = pokemon_request.category,
        description=pokemon_request.description
    )
    db.add(new_pokemon)
    db.flush()
    # Assign types to the pokemon
    assign_types_to_pokemon(new_pokemon, pokemon_request.type, db)
    db.commit()
    db.refresh(new_pokemon)
    return PokemonResponse.form_orm_pokemon(new_pokemon)

# ---------------------------
# DELETE endpoints
# ---------------------------
#Endpoint to delete a Pokemon by id
@router.delete("/{id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_pokemon(id: int, db: db_dependency, user: admin_dependency):
    if user is None:
        raise HTTPException(status_code=401, detail="Unauthorized")
    pokemon_to_delete = db.query(Pokemons).filter(Pokemons.id == id).first()
    if not pokemon_to_delete:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Pokemon not found")
    db.delete(pokemon_to_delete)
    db.commit()
    return Response(status_code=status.HTTP_204_NO_CONTENT)

# ---------------------------
# PUT endpoints
# ---------------------------
#Endpoint to update a Pokemon by id
@router.put("/{id}", status_code=status.HTTP_204_NO_CONTENT)
async def update_pokemon(id: int, pokemon_request: pokemon_create_request_dependency, db:db_dependency, user: admin_dependency):
    if user is None:
        raise HTTPException(status_code=401, detail="Unauthorized")
    pokemon_to_update = db.query(Pokemons).filter(Pokemons.id == id).first()
    if not pokemon_to_update:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Pokemon not found")
    # Update basic fields
    pokemon_to_update.name = pokemon_request.name
    pokemon_to_update.height = pokemon_request.height
    pokemon_to_update.weight = pokemon_request.weight
    pokemon_to_update.category = pokemon_request.category
    pokemon_to_update.description = pokemon_request.description
    # Clear existing types
    pokemon_to_update.types.clear()
    # Assign new types
    assign_types_to_pokemon(pokemon_to_update, pokemon_request.type, db)
    db.commit()
    return Response(status_code=status.HTTP_204_NO_CONTENT)






