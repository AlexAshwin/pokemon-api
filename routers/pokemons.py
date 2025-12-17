from sqlalchemy.orm import Session
from typing import Annotated

from routers.auth import get_current_user
from database import SessionLocal
from models import pokemons, types, pokemon_type

from fastapi import APIRouter, Depends, HTTPException, status, Response, Form
from pydantic import BaseModel, Field

router = APIRouter(
    prefix="/pokemons",
    tags=["pokemons"]
)

# ---------------------------
# Schema
# ---------------------------

class PokemonResponse(BaseModel):
    id: int = Field(..., example=1)
    name: str = Field(..., example="Bulbasaur")
    type: list[str] = Field(..., example=["Grass", "Poison"])
    category: str = Field(..., example="Seed")
    height: float = Field(..., example="0.4")
    weight: float = Field(..., example="6")
    description: str = Field(..., example="A strange seed was planted on its back at birth. "
                                     "The plant sprouts and grows with this Pokémon.")
    model_config = {
        "from_attributes": True
    }

class PokemonCreateRequest(BaseModel):
    name: str = Field(..., min_length=3, max_length=50, example="Bulbasaur")
    type: str = Field(..., example="Grass,Poison")
    category: str = Field(..., min_length=3, max_length=50, example="Seed")
    height: float = Field(..., gt=0, example="0.4")
    weight: float = Field(..., gt=0, example="6")
    description: str = Field(..., min_length=10, max_length=300,
                             example="A strange seed was planted on its back at birth. "
                                     "The plant sprouts and grows with this Pokémon.")
    model_config = {
        "from_attributes": True
    }
    @classmethod
    def as_form(
        cls,
        name: str = Form(..., min_length=3, max_length=50, description="Bulbasaur"),
        type: str = Form(..., description="Grass, Poison"),
        category: str = Form(..., min_length=3, max_length=50, description="Seed"),
        height: float = Form(..., gt=0, description="0.4"),
        weight: float = Form(..., gt=0, description="6"),
        description: str = Form(..., min_length=10, max_length=300,
                             description="A strange seed was planted on its back at birth. "
                                     "The plant sprouts and grows with this Pokémon."),
    ):
        return cls(
            name=name,
            type=type,
            category=category,
            height=height,
            weight=weight,
            description=description
        )

# ---------------------------
# Helpers
# ---------------------------
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

def serialize_pokemon(pokemon_obj):
    return {
        'id': pokemon_obj.id,
        'name': pokemon_obj.name,
        'type': [t.name for t in pokemon_obj.types],
        'category': pokemon_obj.category,
        'height': pokemon_obj.height,
        'weight': pokemon_obj.weight,
        'description': pokemon_obj.description
    }


db_dependency = Annotated[Session,Depends(get_db)]
pokemon_create_request_dependency = Annotated[PokemonCreateRequest, Depends(PokemonCreateRequest.as_form)]
user_dependency = Annotated[dict, Depends(get_current_user)]

# ---------------------------
# Private API
# ---------------------------
    
# Helper function to assign types to a pokemon
def assign_types_to_pokemon(pokemon_obj, type_names, db):
    type_names = [t.strip() for t in type_names.split(",")]
    if len(type_names) > 2:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="A pokemon can have at most 2 types")
    for index, type_name in enumerate(type_names):
        type_obj = db.query(types).filter(types.name == type_name).first()
        if not type_obj:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"Type '{type_name}' not found")
        PokemonType = pokemon_type(pokemon_id=pokemon_obj.id, type_id=type_obj.id, slot=index + 1)
        db.add(PokemonType)

# ---------------------------
# Post endpoints
# ---------------------------
#Endpoints to add pokemons
@router.post("/")
async def create_pokemon(self,pokemon_request: pokemon_create_request_dependency, db: db_dependency, user: user_dependency):
    if user is None:
        raise HTTPException(status_code=401, detail="Unauthorized")
    existing_pokemon = db.query(pokemons).filter(pokemons.name == pokemon_request.name).first()
    if existing_pokemon:
        raise HTTPException(status_code=status.HTTP_409_CONFLICT, detail="Pokemon already exists")
    # Create pokemon entry
    new_pokemon = pokemons(
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
    return new_pokemon

# ---------------------------
# DELETE endpoints
# ---------------------------
#Endpoint to delete a Pokemon by id
@router.delete("/{id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_pokemon(self,id: int, db: db_dependency, user: user_dependency):
    if user is None:
        raise HTTPException(status_code=401, detail="Unauthorized")
    pokemon_to_delete = db.query(pokemons).filter(pokemons.id == id).first()
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
async def update_pokemon(self,id: int, pokemon_request: PokemonCreateRequest, db:db_dependency, user: user_dependency):
    if user is None:
        raise HTTPException(status_code=401, detail="Unauthorized")
    pokemon_to_update = db.query(pokemons).filter(pokemons.id == id).first()
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


# ---------------------------
# GET endpoints
# ---------------------------
# Endpoint to get all Pokemons
@router.get("/", response_model=list[PokemonResponse], status_code=status.HTTP_200_OK)
async def get_all_pokemons(db: db_dependency):
    pokemons_list = db.query(pokemons).all()
    return [serialize_pokemon(p) for p in pokemons_list]

# Endpoint to get a Pokemon by id
@router.get("/{id}", response_model=PokemonResponse, status_code=status.HTTP_200_OK)
async def get_pokemon_by_id(id: int, db: db_dependency):
    pokemon_obj =  db.query(pokemons).filter(pokemons.id == id).first()
    if not pokemon_obj:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Pokemon id not found")
    return serialize_pokemon(pokemon_obj)

# Endpoint to get a Pokemon by name
@router.get("/name/{name}", response_model=PokemonResponse, status_code=status.HTTP_200_OK)
async def get_pokemon_by_name(name: str, db: db_dependency):
    pokemon_obj = db.query(pokemons).filter(pokemons.name == name).first()
    if not pokemon_obj:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Pokemon name not found")
    return serialize_pokemon(pokemon_obj)

# Endpoint to get Pokemons by type
@router.get("/type/{type_name}", response_model=list[PokemonResponse], status_code=status.HTTP_200_OK)
async def get_pokemons_by_type(type_name: str, db: db_dependency):
    type_obj = db.query(types).filter(types.name == type_name).first()
    if not type_obj:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Type not found")
    pokemons_list = type_obj.pokemons
    return [serialize_pokemon(p) for p in pokemons_list]
