from fastapi import FastAPI, Response, HTTPException, Request
from models import models

import uuid
import hashlib
import hmac
import itsdangerous

app = FastAPI()

secret_key = "secret_key"

user = {
    "username": "user123",
    "password": "pass123"
}


def sign_token(user_id: str, secret_key: str):
    signature = hmac.new(
        secret_key.encode(),
        user_id.encode(),
        hashlib.sha256
    ).hexdigest()

    return f"{user_id}.{signature}"


@app.post("/login")
async def login(login_data: models.Login, response: Response):
    if login_data.username != user["username"] or login_data.password != user["password"]:
        raise HTTPException(status_code=401, detail="Incorrect username or password")

    user_id = str(uuid.uuid4())
    session_token = sign_token(user_id, secret_key)
    response.set_cookie(
        key="session_token",
        value=session_token,
        httponly=True,
        max_age=100
    )
    return {"session_token": session_token}

@app.get("/user")
async def get_user(request: Request):
    if request.cookies.get("session_token"):
        return {"username": user["username"], "password": user["password"]}

    raise HTTPException(status_code=401, detail="Unauthorized")

@app.get("profile")
async def get_profile(request: Request):
    session_token = request.cookies.get("session_token")
    if session_token:


