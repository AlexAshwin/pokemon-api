from app.schemas.types import TypeResponse
from app.core.dependencies import type_service_dependency
from app.models.types import Types

from fastapi import APIRouter, status
from sqlalchemy.orm import selectinload

router = APIRouter(
    prefix="/types",
    tags=["types"]
)

# ---------------------------
# Get Endpoints
# ---------------------------
# Endpoint to get all Pokemon types
@router.get("/", response_model=list[TypeResponse], status_code=status.HTTP_200_OK)
async def get_all_types(service: type_service_dependency):
    types_list = service.get_all_types(relations=[selectinload(Types.pokemon_types)])
    return [TypeResponse.form_orm_type(id=type_obj.id, name=type_obj.name) for type_obj in types_list]


# Endpoint to get a Pokemon type by id
@router.get("/{id}", response_model=TypeResponse, status_code=status.HTTP_200_OK)
async def get_type_by_id(id: int, service: type_service_dependency):
    type_obj = service.get_type_by_id(id, relations=[selectinload(Types.pokemon_types)])
    return TypeResponse.form_orm_type(id=type_obj.id, name=type_obj.name)


