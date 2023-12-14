from fastapi import FastAPI
import uvicorn
from fastapi.responses import JSONResponse

app = FastAPI()

@app.get("/")
def health_check():
    return JSONResponse(content={"status": "Running!!!"})

if __name__ == '__main__':
    
    uvicorn.run("main:app", 
                host="localhost", 
                port=8000, 
                reload=True)