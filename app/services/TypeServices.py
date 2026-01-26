from fastapi import HTTPException, status
from sqlalchemy.orm import selectinload

from app.services.BaseServices import BaseService
from app.models.types import Types


class TypeService(BaseService):
    def __init__(self, db):
        super().__init__(db)

    def get_all_types(self, relations=None):
        return self.get_all_obj(model=Types, relations=relations)

    def get_type_by_id(self, type_id: int, relations=None):
        return self.get_single_obj(model=Types, attribute_name="id", attribute_value=type_id,
                                   relations=relations)

    def get_type_by_name(self, type_name: str, relations=None):
        return self.get_single_obj(model=Types, attribute_name="name", attribute_value=type_name, relations=relations)

    def type_exists(self, name: str) -> bool:
        return self.exists_by(model=Types, attribute_name="name", value=name)

    def create_type(self, name):
        try:
            type_obj = Types(name=name)
            self.db.add(type_obj)
            self.db.commit()
            self.db.refresh(type_obj)
            return type_obj
        except Exception as e:
            self.db.rollback()
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail=f"Error while creating type: {e}"
            )

    def update_type(self, id:int, name:str):
        type_to_update = self.get_type_by_id(type_id=id)
        if self.type_exists(name):
            raise HTTPException(
                status_code=status.HTTP_409_CONFLICT,
                detail="Type already exists"
            )
        try:
            type_to_update.name = name
            self.db.commit()
        except Exception as e:
            self.db.rollback()
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail=f"Error while updating type: {e}"
            )

    def delete_type(self, id:int):
        type_to_delete = self.get_type_by_id(type_id=id)
        if type_to_delete.pokemon_types:
            raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST,
                                detail="Cannot delete type assigned to Pokemons")
        if type_to_delete.attacks or type_to_delete.defenses:
            raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST,
                                detail="Cannot delete type assigned to Type Effectiveness")
        try:
            self.db.delete(type_to_delete)
            self.db.commit()
        except Exception as e:
            self.db.rollback()
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail=f"Error while deleting type: {e}"
            )
