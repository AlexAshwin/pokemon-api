from fastapi import APIRouter, HTTPException, status, Response

from app.models.types import Types
from app.schemas.types import TypeResponse, TypeCreateRequest
from app.core.dependencies import db_dependency, admin_dependency

router = APIRouter(
    prefix="/types",
    tags=["types"]
)


# ---------------------------
# POST Endpoints
# ---------------------------
# Endpoint to create a new Pokemon type
@router.post("/", response_model=TypeResponse, status_code=status.HTTP_201_CREATED)
async def create_pokemon_type(type_request: TypeCreateRequest, db: db_dependency, user: admin_dependency):
    if user is None:
        raise HTTPException(status_code=401, detail="Unauthorized")
    existing_type = db.query(Types).filter(Types.name == type_request.name).first()
    if existing_type:
        raise HTTPException(status_code=status.HTTP_409_CONFLICT, detail="Type already exists")
    new_type = Types(name=type_request.name)
    db.add(new_type)
    db.commit()
    db.refresh(new_type)
    return new_type


# ---------------------------
# PUT Endpoints
# ---------------------------
# Endpoint to update a Pokemon type by id
@router.put("/{id}", status_code=status.HTTP_204_NO_CONTENT)
async def update_pokemon_type(id: int, type_request: TypeCreateRequest, db: db_dependency, user: admin_dependency):
    if user is None:
        raise HTTPException(status_code=401, detail="Unauthorized")
    type_to_update = db.query(Types).filter(Types.id == id).first()
    if not type_to_update:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Type not found")
    type_to_update.name = type_request.name
    db.commit()
    return Response(status_code=status.HTTP_204_NO_CONTENT)


# ---------------------------
# DELETE Endpoints
# ---------------------------
# Endpoint to delete a Pokemon type by name
@router.delete("/{id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_pokemon_type(id: int, db: db_dependency, user: admin_dependency):
    if user is None:
        raise HTTPException(status_code=401, detail="Unauthorized")
    type_to_delete = db.query(Types).filter(Types.id == id).first()
    if not type_to_delete:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Type not found")
    if type_to_delete.pokemon_types:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Cannot delete type assigned to Pokemons")
    db.delete(type_to_delete)
    db.commit()
    return Response(status_code=status.HTTP_204_NO_CONTENT)
