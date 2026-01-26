from typing import Annotated
from sqlalchemy.orm import Session
from fastapi import Depends

from app.core.database import get_db
from app.core.security import get_current_user
from app.schemas.pokemons import *
from app.schemas.types import *
from app.schemas.type_effectiveness import *
from app.services.PokemonService import PokemonService
from app.services.TypeServices import TypeService
from app.services.TypeEffectivenessService import TypeEffectivenessService

def get_pokemon_service(db: Session = Depends(get_db)) -> PokemonService:
    return PokemonService(db)

def get_type_service(db: Session = Depends(get_db)) -> TypeService:
    return TypeService(db)

def get_type_effectiveness_service(db:Session = Depends(get_db)) -> TypeEffectivenessService:
    return TypeEffectivenessService(db)

#aliases for dependencies
db_dependency = Annotated[Session, Depends(get_db)]
admin_dependency = Annotated[dict, Depends(get_current_user)]

pokemon_service_dependency = Annotated[PokemonService, Depends(get_pokemon_service)]
pokemon_create_request_dependency = Annotated[PokemonCreateRequest, Depends(PokemonCreateRequest.as_form)]
pokemon_update_request_dependency = Annotated[PokemonUpdateRequest,Depends(PokemonUpdateRequest.as_form)]

type_service_dependency = Annotated[TypeService, Depends(get_type_service)]
type_create_request_dependency = Annotated[TypeCreateRequest, Depends(TypeCreateRequest.as_form)]

type_effectiveness_service_dependency = Annotated[TypeEffectivenessService,Depends(get_type_effectiveness_service)]
type_effectiveness_create_request_dependency = Annotated[TypeEffectivenessCreateRequest, Depends(TypeEffectivenessCreateRequest.as_form)]