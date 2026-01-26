from fastapi import APIRouter, HTTPException, status
from typing import List

from app.core.dependencies import type_effectiveness_service_dependency
from app.schemas.type_effectiveness import TypeEffectivenessResponse

router = APIRouter(
    prefix="/type-effectiveness",
    tags=["type-effectiveness"]
)


# ---------------------------
# GET Endpoints
# ---------------------------
@router.get("/", response_model=List[TypeEffectivenessResponse], status_code=status.HTTP_200_OK)
async def get_all_attacking_type_effectiveness(service: type_effectiveness_service_dependency):
    all_type_effectiveness = service.get_all_type_effectiveness()
    return [TypeEffectivenessResponse.from_orm_type_effectiveness(attacking_type=type_obj, rows=attack_rows) for
            type_obj, attack_rows in all_type_effectiveness]


@router.get("/attacking_type_name", status_code=status.HTTP_200_OK)
async def get_attacking_type_effectiveness(name: str, service: type_effectiveness_service_dependency):
    type_obj, attack_rows = service.get_attacking_type_effectiveness(attribute_value=name)
    if not attack_rows:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Type effectiveness for {name} not found"
        )
    return TypeEffectivenessResponse.from_orm_type_effectiveness(attacking_type=type_obj,rows=attack_rows)

