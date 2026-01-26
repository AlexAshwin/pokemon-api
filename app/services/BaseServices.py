from fastapi import HTTPException, status
from sqlalchemy.orm import selectinload
from sqlalchemy.sql import exists


class BaseService:
    def __init__(self, db):
        self.db = db

    # -------------------------
    # Internal helpers
    # -------------------------
    def _get_column(self, model, attr: str):
        if not hasattr(model, attr):
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail=f"{model.__name__} has no attribute '{attr}'"
            )
        return getattr(model, attr)

    def _base_query(self, model, relations: None):
        query = self.db.query(model)
        if relations:
            for option in relations:
                query = query.options(option)
        return query

    # -------------------------
    # Read operations
    # -------------------------
    def get_single_obj(self, model, attribute_name, attribute_value, *, ilike=False, relations=None):
        column = self._get_column(model, attribute_name)
        query = self._base_query(model, relations)
        if ilike:
            query = query.filter(column.ilike(f"%{attribute_value}%"))
        else:
            query = query.filter(column == attribute_value)
        obj = query.first()
        if not obj:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                                detail=f"{model.__name__} with {attribute_name} '{attribute_value}' not found")
        return obj

    def get_multiple_objs(self, model, attribute_name, attribute_values, *, relations=None):
        attribute_values = set(attribute_values)
        column = self._get_column(model, attribute_name)
        objs = (
            self._base_query(model, relations)
            .filter(column.in_(attribute_values))
            .all()
        )
        found_values = {getattr(obj, attribute_name) for obj in objs}
        missing_values = attribute_values - found_values
        if missing_values:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=f"{model.__name__} with {attribute_name}s '{', '.join(missing_values)}' not found"
            )
        return objs

    def get_all_obj(self, model, *, relations=None):
        return self._base_query(model, relations).all()

    # -------------------------
    # Exists
    # -------------------------
    def exists_by(self, model, attribute_name, value) -> bool:
        column = self._get_column(model, attribute_name)
        return self.db.query(exists().where(column == value)).scalar()
