from fastapi import status, HTTPException
from pydantic import BaseModel, model_validator
from typing import List, Optional, Dict, Set
from fastapi import Form


class TypeEffectivenessBase(BaseModel):
    type_name: str


class TypeEffectivenessResponse(TypeEffectivenessBase):
    strong_against: Dict[str, float]
    weak_against: Dict[str, float]
    immune_against: Dict[str, float]
    neutral_against: Dict[str, float]

    @classmethod
    def from_orm_type_effectiveness(cls, attacking_type, rows):
        strong, weak, no_effect, neutral = {}, {}, {}, {}
        for row in rows:
            entry = {row.defending_type.name: row.effectiveness_multiplier}
            if row.effectiveness_multiplier > 1:
                strong.update(entry)
            elif row.effectiveness_multiplier == 0:
                no_effect.update(entry)
            elif row.effectiveness_multiplier < 1:
                weak.update(entry)
            else:
                neutral.update(entry)

        return cls(
            type_name=attacking_type.name,
            strong_against=strong,
            weak_against=weak,
            immune_against=no_effect,
            neutral_against=neutral
        )


class TypeEffectivenessCreateRequest(TypeEffectivenessBase):
    strong_against: Set[str] = set()
    weak_against: Set[str] = set()
    no_effect_against: Set[str] = set()

    @classmethod
    def as_form(
            cls,
            type_name: str = Form(..., description="Fire"),
            strong_against: Optional[str] = Form(None, description="Grass, Ice, Bug, Steel"),
            weak_against: Optional[str] = Form(None, description="Water, Rock, Fire"),
            no_effect_against: Optional[str] = Form(None, description="")
    ):
        def normalize(value: Optional[str]) -> Set[str]:
            if not value:
                return set()
            return {v.strip().title() for v in value.split(",") if v.strip()}

        return cls(
            type_name=type_name.strip().title(),
            strong_against=normalize(strong_against),
            weak_against=normalize(weak_against),
            no_effect_against=normalize(no_effect_against),
        )

    @model_validator(mode="after")
    def validate_overlaps(self):
        overlap = (
                self.strong_against & self.weak_against
                | self.strong_against & self.no_effect_against
                | self.weak_against & self.no_effect_against
        )
        if overlap:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail=f"Type(s) {', '.join(overlap)} cannot appear in multiple effectiveness categories"
            )
        return self
