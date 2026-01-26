from fastapi import APIRouter, HTTPException, status

from app.core.dependencies import type_effectiveness_service_dependency, admin_dependency, \
    type_effectiveness_create_request_dependency
from app.services.TypeEffectivenessService import *
from app.schemas.type_effectiveness import TypeEffectivenessResponse

router = APIRouter(
    prefix="/type-effectiveness",
    tags=["type-effectiveness"]
)


# ---------------------------
# POST Endpoints
# ---------------------------
# Endpoint to create type effectiveness entries
@router.post("/", response_model=TypeEffectivenessResponse, status_code=status.HTTP_201_CREATED)
async def create_type_effectiveness(type_effectiveness_request: type_effectiveness_create_request_dependency,
                                    service: type_effectiveness_service_dependency):
    attacking_type_obj = service.get_type_by_name(type_effectiveness_request.type_name)
    if service.check_if_type_effectiveness_exists(attribute_name="attacking_type_id",
                                                  attribute_value=attacking_type_obj.id):
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST,
                            detail=f"Type effectiveness data for type '{type_effectiveness_request.type_name}' already exists")
    rows = service.create_type_effectiveness(attacking_type=attacking_type_obj, request=type_effectiveness_request)
    return TypeEffectivenessResponse.from_orm_type_effectiveness(attacking_type=attacking_type_obj, rows=rows)


@router.put("/", response_model=TypeEffectivenessResponse, status_code=status.HTTP_201_CREATED)
async def update_type_effectiveness(type_effectiveness_request: type_effectiveness_create_request_dependency,
                                    service: type_effectiveness_service_dependency):
    attacking_type_obj = service.get_type_by_name(type_effectiveness_request.type_name)
    if service.check_if_type_effectiveness_exists(attribute_name="attacking_type_id",
                                                  attribute_value=attacking_type_obj.id) == False:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST,
                            detail=f"Type effectiveness data for type '{type_effectiveness_request.type_name}' doesn't exists")
    rows = service.update_type_effectiveness(attacking_type=attacking_type_obj, request=type_effectiveness_request)
    return TypeEffectivenessResponse.from_orm_type_effectiveness(attacking_type=attacking_type_obj, rows=rows)
