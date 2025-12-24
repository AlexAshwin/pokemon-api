from fastapi import FastAPI, status

from routers.Public import pokemons as public_pokemons
from routers.Public import types as public_types
from routers.Private import pokemons as private_pokemons
from routers.Private import types as private_types
from routers.Private import auth
app = FastAPI()

@app.get("/ping", status_code=status.HTTP_200_OK)
def ping():
    return {"message": "pong!"}

#routes would be included here
app.include_router(auth.router)
app.include_router(public_types.router)
app.include_router(private_types.router)
app.include_router(public_pokemons.router)
app.include_router(private_pokemons.router)