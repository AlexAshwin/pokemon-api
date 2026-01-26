from fastapi import APIRouter, HTTPException, status, Response

from app.core.dependencies import admin_dependency, pokemon_create_request_dependency, \
    pokemon_service_dependency, pokemon_update_request_dependency
from app.schemas.pokemons import PokemonResponse

router = APIRouter(
    prefix="/pokemons",
    tags=["pokemons"]
)

# ---------------------------
# Post endpoints
# ---------------------------
# Endpoints to add pokemons
@router.post("/", response_model=PokemonResponse, status_code=status.HTTP_201_CREATED)
async def create_pokemon(pokemon_request: pokemon_create_request_dependency, service: pokemon_service_dependency,
                         user: admin_dependency):
    if service.check_if_pokemon_exists(name=pokemon_request.name):
        raise HTTPException(status_code=status.HTTP_409_CONFLICT,
                            detail=f"Pokemon with name {pokemon_request.name} already exists")
    new_pokemon = service.create_pokemon(pokemon_request)
    return PokemonResponse.form_orm_pokemon(new_pokemon)

# ---------------------------
# DELETE endpoints
# ---------------------------
# Endpoint to delete a Pokemon by id
@router.delete("/{id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_pokemon(id: int, service: pokemon_service_dependency, user: admin_dependency):
    pokemon_to_delete = service.get_pokemon_by_id(pokemon_id=id)
    service.delete_pokemon(pokemon_obj=pokemon_to_delete)
    return Response(status_code=status.HTTP_204_NO_CONTENT)

# ---------------------------
# Patch endpoints
# ---------------------------
# Endpoint to update a Pokemon by id
@router.patch("/{id}", status_code=status.HTTP_204_NO_CONTENT)
async def update_pokemon(id: int, service: pokemon_service_dependency,
                         pokemon_request: pokemon_update_request_dependency,
                         user: admin_dependency):
    if pokemon_request.name is not None:
        if service.check_if_pokemon_exists(name=pokemon_request.name):
            raise HTTPException(status_code=status.HTTP_409_CONFLICT,
                                detail=f"Pokemon with name {pokemon_request.name} already exists")
    service.update_pokemon(id=id, pokemon_request=pokemon_request)
    return Response(status_code=status.HTTP_204_NO_CONTENT)

