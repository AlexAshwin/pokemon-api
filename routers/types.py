from typing import Annotated
from database import SessionLocal
from sqlalchemy.orm import Session
from models import types
from routers.auth import get_current_user
from fastapi import APIRouter, Depends, HTTPException, status, Response
from pydantic import BaseModel

router = APIRouter(
    prefix="/types",
    tags=["types"]
)


# ---------------------------
# Helper Functions
# ---------------------------
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


db_dependency = Annotated[Session, Depends(get_db)]
user_dependency = Annotated[dict, Depends(get_current_user)]


# ---------------------------
# Schema
# ---------------------------
class TypeResponse(BaseModel):
    id: int
    name: str
    model_config = {
        "from_attributes": True
    }


class TypeCreateRequest(BaseModel):
    name: str
    model_config = {
        "from_attributes": True
    }


# ---------------------------
# Get Endpoints
# ---------------------------
# Endpoint to get all Pokemon types
@router.get("/", response_model=list[TypeResponse], status_code=status.HTTP_200_OK)
async def get_all_types(db: db_dependency):
    types_list = db.query(types).all()
    return types_list


# Endpoint to get a Pokemon type by id
@router.get("/{id}", response_model=TypeResponse, status_code=status.HTTP_200_OK)
async def get_type_by_id(id: int, db: db_dependency):
    type_obj = db.query(types).filter(types.id == id).first()
    if not type_obj:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Type not found")
    return type_obj


# ---------------------------
# POST Endpoints
# ---------------------------
# Endpoint to create a new Pokemon type
@router.post("/", response_model=TypeResponse, status_code=status.HTTP_201_CREATED)
async def create_pokemon_type(type_request: TypeCreateRequest, db: db_dependency, user: user_dependency):
    if user is None:
        raise HTTPException(status_code=401, detail="Unauthorized")
    existing_type = db.query(types).filter(types.name == type_request.name).first()
    if existing_type:
        raise HTTPException(status_code=status.HTTP_409_CONFLICT, detail="Type already exists")
    new_type = types(name=type_request.name)
    db.add(new_type)
    db.commit()
    db.refresh(new_type)
    return new_type


# ---------------------------
# PUT Endpoints
# ---------------------------
# Endpoint to update a Pokemon type by id
@router.put("/{id}", status_code=status.HTTP_204_NO_CONTENT)
async def update_pokemon_type(id: int, type_request: TypeCreateRequest, db: db_dependency, user: user_dependency):
    if user is None:
        raise HTTPException(status_code=401, detail="Unauthorized")
    type_to_update = db.query(types).filter(types.id == id).first()
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
async def delete_pokemon_type(id: int, db: db_dependency, user: user_dependency):
    if user is None:
        raise HTTPException(status_code=401, detail="Unauthorized")
    type_to_delete = db.query(types).filter(types.id == id).first()
    if not type_to_delete:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Type not found")
    if type_to_delete.pokemon_types:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Cannot delete type assigned to Pokemons")
    db.delete(type_to_delete)
    db.commit()
    return Response(status_code=status.HTTP_204_NO_CONTENT)
