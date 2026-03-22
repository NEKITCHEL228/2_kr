from fastapi import FastAPI, Request, HTTPException, Header, Response
from models.models import CommonHeaders
from typing import Annotated
from datetime import datetime

app = FastAPI()

@app.get("/headers")
async def get_headers(headers: Annotated[CommonHeaders, Header(...)]):
    user_agent = headers.user_agent
    
    if not user_agent:
        raise HTTPException(status_code=400, detail="Missing 'User-Agent' headers")
    
    accept_language = headers.accept_language
    
    if not accept_language:
        raise HTTPException(status_code=400, detail="Missing 'Accept-Language' headers")
    
    return {"User-Agent": user_agent, "Accept-Language": accept_language}

@app.get("/info")
async def get_info(headers: Annotated[CommonHeaders, Header(...)], response: Response):
    user_agent = headers.user_agent
    response.headers["X-Server-Time"] = str(datetime.now())
    
    if not user_agent:
        raise HTTPException(status_code=400, detail="Missing 'User-Agent' headers")
    
    accept_language = headers.accept_language
    
    if not accept_language:
        raise HTTPException(status_code=400, detail="Missing 'Accept-Language' headers")
    
    return {"message": "Добро пожаловать! Ваши заголовки успешно обработаны.", "headers": {"User-Agent": user_agent, "Accept-Language": accept_language}}