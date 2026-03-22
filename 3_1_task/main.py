from fastapi import FastAPI
from models import models

app = FastAPI()

fake_bd = []

@app.post("/create_user")
async def send_feedback(user: models.UserCreate):
    fake_bd.append(user)
    return user.dict()