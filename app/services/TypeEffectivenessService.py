from fastapi import status, HTTPException

from app.services.TypeServices import TypeService
from app.models.type_effectiveness import TypeEffectiveness
from app.models.types import Types


class TypeEffectivenessService(TypeService):
    def __init__(self, db):
        super().__init__(db)

    def get_attacking_type_effectiveness(self, attribute_value):
        type_obj = self.get_type_by_name(attribute_value)
        return type_obj, type_obj.attacks

    def check_if_type_effectiveness_exists(self, attribute_name, attribute_value) -> bool:
        return self.exists_by(model=TypeEffectiveness, attribute_name=attribute_name,
                              value=attribute_value) is True

    def get_all_type_effectiveness(self):
        types = self.get_all_types()
        return [(type_obj, type_obj.attacks) for type_obj in types]

    def resolve_types(self, type_names: list[str], type_map: dict[str, Types], multiplier: float) -> dict[Types, float]:
        resolved = {}
        for name in type_names:
            key = name.capitalize()
            if key not in type_map:
                raise HTTPException(
                    status_code=status.HTTP_404_NOT_FOUND,
                    detail=f"'{name}' is not a valid type"
                )
            resolved[type_map[key]] = multiplier
        return resolved

    def create_type_effectiveness(self, attacking_type: Types, request):
        all_types = self.get_all_types()
        type_map = {t.name: t for t in all_types}
        effectiveness = {}
        mappings = [
            (request.strong_against, 2),
            (request.weak_against, 0.5),
            (request.no_effect_against, 0),
        ]
        # Resolve provided types
        for type_list, multiplier in mappings:
            effectiveness.update(
                self.resolve_types(type_list, type_map, multiplier)
            )
        # Compute neutral from DB (difference)
        for t in all_types:
            effectiveness.setdefault(t, 1)
        try:
            self.db.add_all(
                TypeEffectiveness(
                    attacking_type_id=attacking_type.id,
                    defending_type_id=def_type.id,
                    effectiveness_multiplier=multiplier
                )
                for def_type, multiplier in effectiveness.items()
            )
            self.db.commit()
        except Exception as e:
            self.db.rollback()
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail=str(e)
            )
        return attacking_type.attacks

    def update_type_effectiveness(self,attacking_type: Types, request):
        all_types= self.get_all_types()
        type_map = {t.name:t for t in all_types}
        existing_rows = {
            te.defending_type: te
            for te in self.get_attacking_type_effectiveness(attacking_type.name)
        }
        desired  = {}
        desired.update(self.resolve_types(request.strong_against, type_map,2))
        desired.update(self.resolve_types(request.weak_against, type_map, 0.5))
        desired.update(self.resolve_types(request.no_effect_against, type_map, 0))
        for t in all_types:
            desired.setdefault(t,1)
        try:
            for def_type, te in existing_rows.items():
                te.effectiveness_multiplier  = desired[def_type]
            self.db.commit()
        except Exception as e:
            self.db.rollback()
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail = f"Update failed due to error {e}"
            )
        return attacking_type.attacks