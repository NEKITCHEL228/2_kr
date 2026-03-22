from fastapi import FastAPI, Request, HTTPException

app = FastAPI()

@app.get("/headers")
async def get_headers(request: Request):
    headers = request.headers
    user_agent = headers.get("User-agent")
    
    if not user_agent:
        raise HTTPException(status_code=400, detail="Missing 'User-Agent' headers")
    
    accept_language = headers.get("Accept-Language")
    
    if not accept_language:
        raise HTTPException(status_code=400, detail="Missing 'Accept-Language' headers")
    
    return {"User-Agent": user_agent, "Accept-Language": accept_language}