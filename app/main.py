from fastapi import FastAPI, status

from app.routers.Public import pokemons as public_pokemons, types as public_types, \
    type_effectivness as public_type_effectiveness
from app.routers.Private import pokemons as private_pokemons, auth, types as private_types, \
    type_effectiveness as private_type_effectiveness

app = FastAPI()


@app.get("/ping", status_code=status.HTTP_200_OK)
def ping():
    return {"message": "pong!"}


# routes would be included here
app.include_router(auth.router)
app.include_router(public_types.router)
app.include_router(private_types.router)
app.include_router(public_pokemons.router)
app.include_router(private_pokemons.router)
#app.include_router(private_type_effectiveness.router)
app.include_router(public_type_effectiveness.router)