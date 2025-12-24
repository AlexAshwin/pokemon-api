from app.models.types import Types
from app.schemas.types import TypeResponse
from app.core.dependencies import db_dependency

from fastapi import APIRouter, HTTPException, status

router = APIRouter(
    prefix="/types",
    tags=["types"]
)

# ---------------------------
# Get Endpoints
# ---------------------------
# Endpoint to get all Pokemon types
@router.get("/", response_model=list[TypeResponse], status_code=status.HTTP_200_OK)
async def get_all_types(db: db_dependency):
    types_list = db.query(Types).all()
    return types_list


# Endpoint to get a Pokemon type by id
@router.get("/{id}", response_model=TypeResponse, status_code=status.HTTP_200_OK)
async def get_type_by_id(id: int, db: db_dependency):
    type_obj = db.query(Types).filter(Types.id == id).first()
    if not type_obj:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Type not found")
    return type_obj

