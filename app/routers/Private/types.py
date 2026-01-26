from fastapi import APIRouter, HTTPException, status, Response

from app.core.dependencies import admin_dependency, type_service_dependency, type_create_request_dependency
from app.schemas.types import TypeResponse, TypeCreateRequest

router = APIRouter(
    prefix="/types",
    tags=["types"]
)


# ---------------------------
# POST Endpoints
# ---------------------------
# Endpoint to create a new Pokemon type
@router.post("/", response_model=TypeResponse, status_code=status.HTTP_201_CREATED)
async def create_pokemon_type(type_request: type_create_request_dependency, service: type_service_dependency,
                              user: admin_dependency):
    if user is None:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Unauthorized"
        )
    name = type_request.name.capitalize()
    if service.type_exists(name):
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail="Type already exists"
        )
    new_type = service.create_type(name)
    return TypeResponse.form_orm_type(id=new_type.id,name=new_type.name)


# ---------------------------
# PUT Endpoints
# ---------------------------
# Endpoint to update a Pokemon type by id
@router.put("/{id}", status_code=status.HTTP_204_NO_CONTENT)
async def update_pokemon_type(id: int, type_request: type_create_request_dependency, service: type_service_dependency,
                              user: admin_dependency):
    if user is None:
        raise HTTPException(status_code=401, detail="Unauthorized")
    name = type_request.name.capitalize()
    service.update_type(id=id,name=name)
    return Response(status_code=status.HTTP_204_NO_CONTENT)

# ---------------------------
# DELETE Endpoints
# ---------------------------
# Endpoint to delete a Pokemon type by name
@router.delete("/{id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_pokemon_type(id: int, service:type_service_dependency, user: admin_dependency):
    if user is None:
        raise HTTPException(status_code=401, detail="Unauthorized")
    service.delete_type(id=id)
    return Response(status_code=status.HTTP_204_NO_CONTENT)
