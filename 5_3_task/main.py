from fastapi import FastAPI, Response, HTTPException, Request
from models import models

import uuid
import time
from itsdangerous import BadSignature, SignatureExpired, URLSafeTimedSerializer

app = FastAPI()

secret_key = "secret_key"
s = URLSafeTimedSerializer(secret_key)

user = {
    "username": "user123",
    "password": "pass123"
}


@app.post("/login")
async def login(login_data: models.Login, response: Response):
    if login_data.username != user["username"] or login_data.password != user["password"]:
        raise HTTPException(status_code=401, detail="Incorrect username or password")

    user_id = str(uuid.uuid4())
    
    session_token = s.dumps({ "user_id": user_id, "last_activity": int(time.time()) })
    
    response.set_cookie(
        key="session_token",
        value=session_token,
        httponly=True,
        secure=False,
        max_age=300
    )
    return {"session_token": session_token}

@app.get("/user")
async def get_user(request: Request):
    if request.cookies.get("session_token"):
        return {"username": user["username"], "password": user["password"]}

    raise HTTPException(status_code=401, detail="Unauthorized")

@app.get("/profile")
async def get_profile(request: Request, response: Response):
    session_token = request.cookies.get("session_token")
    
    if not session_token:
        raise HTTPException(status_code=401, detail="Session expired")
    
    try:
        data = s.loads(session_token)
    except BadSignature:
        raise HTTPException(status_code=401, detail="Session expired")
    
    user_id = data["user_id"]
    last_activity = data["last_activity"]
    
    now = int(time.time())
    diff = now - last_activity
    
    if diff > 300:
        raise HTTPException(status_code=401, detail="Session expired")
    
    if 180 <= diff <= 300:
        new_token =  s.dumps({ "user_id": user_id, "last_activity": now })
        
        response.set_cookie(
            key="session_token",
            value=new_token,
            httponly=True,
            secure=False,
            max_age=300
        )
    
    return {"user_id": user_id, "username": user["username"]}

