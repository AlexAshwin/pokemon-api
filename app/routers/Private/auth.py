import json
from datetime import timedelta
from fastapi import Depends, HTTPException, status, APIRouter
from fastapi.security import OAuth2PasswordRequestForm

from app.schemas.auth import Token
from app.core.security import create_access_token, ACCESS_TOKEN_EXPIRE_MINUTES

router = APIRouter(
    prefix="/auth",
    tags=["auth"]
)

def load_users():
    with open("user.json") as f:
        data = json.load(f)
    return {u["username"]: u for u in data["users"]}


def authenticate_user(username: str, password: str):
    users  = load_users()
    user = users.get(username)
    if not user or user["password"] != password:
        return False
    return user

@router.post("/token", response_model=Token, include_in_schema=False)
async def login_for_access_token(form_data: OAuth2PasswordRequestForm = Depends()):
    user = authenticate_user(form_data.username, form_data.password)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect username or password",
            headers={"WWW-Authenticate": "Bearer"},
        )
    access_token_expires = timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    access_token = create_access_token(
        user_name=user["username"], expires_delta=access_token_expires
    )
    return {"access_token": access_token, "token_type": "bearer"}