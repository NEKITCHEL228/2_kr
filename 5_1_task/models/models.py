from pydantic import BaseModel

class Login(BaseModel):
    username: str
    password: str

class User(BaseModel):
    session_token: str