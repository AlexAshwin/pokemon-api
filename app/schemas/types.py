from pydantic import BaseModel

class TypeBase(BaseModel):
    name: str

class TypeResponse(TypeBase):
    id: int

    model_config = {
        "from_attributes": True
    }

class TypeCreateRequest(TypeBase):

    model_config = {
        "from_attributes": True
    }