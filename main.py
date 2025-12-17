from fastapi import FastAPI, status

from routers import types, pokemons, auth

app = FastAPI()

@app.get("/ping", status_code=status.HTTP_200_OK)
def ping():
    return {"message": "pong!"}

#routes would be included here
app.include_router(auth.router)
app.include_router(types.router)
app.include_router(pokemons.router)