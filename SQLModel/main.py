from fastapi import FastAPI
from models.gem_model import *
from repos import gem_repos
from sqlmodel import create_engine, SQLModel
import uvicorn

app = FastAPI()

engine = create_engine('postgresql://postgres:041101@localhost:5432/mysql_db')

def init_db():
    SQLModel.metadata.create_all(engine)

@app.on_event("startup")
def on_startup():
    init_db()
    
    
@app.get("/gems")
def select_gem():    
    gems = gem_repos.select_all_gems()
    return {"gems": gems}
    
    
# @app.get("/gems/{id}")
# def select_gem(id: int):    
#     gems = gem_repos.select_gems(id)
#     return {"gems": gems}


if __name__ == "__main__":
    uvicorn.run("main:app", host='localhost', port=8080, reload=True)