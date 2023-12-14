from fastapi import FastAPI
from redis import Redis
import json
import uvicorn
import httpx

app = FastAPI()

@app.on_event("startup")
async def startup_event():
    """
     Initialize Redis and HTTP client when app is started. This is called by app. __init__
    """
    app.state.redis = Redis(host="localhost", port=6379)
    app.state.http_client = httpx.AsyncClient()
    
@app.on_event("shutdown")
async def shutdown_event():
    app.state.redis.close()
    
@app.get("/entries")
async def read_item():
    value = app.state.redis.get("entries")
    if value is None:
        response = await app.state.http_client.get('https://api.publicapis.org/entries')
        value = response.json()
        data_str = json.dumps(value)
        app.state.redis.set("entries", data_str)
    return json.loads(value)


if __name__ == "__main__":
    uvicorn.run("main:app", host="localhost", port=8080, reload=True)