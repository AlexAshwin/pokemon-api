from fastapi import HTTPException, status

from app.services.BaseServices import BaseService
from app.models.types import Types


class TypeService(BaseService):
    def __init__(self, db):
        super().__init__(db)

    def get_all_types(self):
        return self.get_all_obj(Types)

    def get_type_by_id(self, type_id: int):
        return self.get_single_obj(Types, "id", type_id)

    def get_type_by_name(self, type_name: str):
        return self.get_single_obj(Types, "name", type_name)

    def create_type(self,name):
        try:
            type_obj = Types(name = name)
            self.db.add(type_obj)
            self.db.refresh()
            return type_obj
        except Exception as e:
            self.db.rollback()
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail = f"Error while creating type: str{e}"
            )
