from fastapi import HTTPException, status

from app.models.types import Types
from app.models.type_effectiveness import TypeEffectiveness


def get_single_obj(model_name, attribute_name: str, attribute_value: str, db):
    type_obj = db.query(model_name).filter(getattr(model_name, attribute_name) == attribute_value).first()
    if not type_obj:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f"{model_name.__name__} with {attribute_name} '{attribute_value}' not found")
    return type_obj

def get_multiple_objs(model_name, attribute_name: str, attribute_values: set, db):
    objs = db.query(model_name).filter(getattr(model_name, attribute_name).in_(attribute_values)).all()
    found_values = {getattr(obj, attribute_name) for obj in objs}
    missing_values = attribute_values - found_values
    if missing_values:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f"{model_name.__name__} with {attribute_name}s '{', '.join(missing_values)}' not found")
    return objs

def get_all_obj(model_name, db):
    return db.query(model_name).all()