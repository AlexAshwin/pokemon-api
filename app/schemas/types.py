from pydantic import BaseModel
from fastapi import Form

class TypeBase(BaseModel):
    name: str

class TypeResponse(TypeBase):
    id: int

    @classmethod
    def form_orm_type(cls,id, name):
        return cls(
            id= id,
            name = name
        )

class TypeCreateRequest(TypeBase):
    @classmethod
    def as_form(cls,
    name : str = Form(..., min_length=3, max_length=15, description = "Normal")
    ):
        return cls(
            name = name
        )