from fastapi import FastAPI, Response, HTTPException, Request
from models import models

import uuid

app = FastAPI()

user = {
    "username": "user123",
    "password": "pass123"
}

@app.post("/login")
async def login(login_data: models.Login, response: Response):
    if login_data.username != user["username"] or login_data.password != user["password"]:
        raise HTTPException(status_code=401, detail="Incorrect username or password")

    session_token = str(uuid.uuid4())
    response.set_cookie(
        key="session_token",
        value=session_token,
        max_age=100
    )
    return {"session_token": session_token}

@app.get("/user")
async def get_user(request: Request):
    if request.cookies.get("session_token"):
        return {"username": user["username"], "password": user["password"]}

    raise HTTPException(status_code=401, detail="Unauthorized")