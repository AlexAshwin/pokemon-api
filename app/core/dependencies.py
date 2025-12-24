from typing import Annotated
from sqlalchemy.orm import Session
from fastapi import Depends

from core.database import get_db
from core.security import get_current_user
from schemas.pokemons import PokemonCreateRequest

db_dependency = Annotated[Session, Depends(get_db)]
admin_dependency = Annotated[dict, Depends(get_current_user)]
pokemon_create_request_dependency = Annotated[PokemonCreateRequest, Depends(PokemonCreateRequest.as_form)]