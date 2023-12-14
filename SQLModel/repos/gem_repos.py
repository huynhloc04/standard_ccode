from main import engine
from models.gem_model import Gem, GemProperties
from sqlmodel import Session, select

def select_all_gems():
    with Session(engine) as session:
        stats = select(Gem, GemProperties).where(Gem.gem_properties_id == GemProperties.id)
        result = session.exec(stats)
        res = []
        for gem, props in result:
            res.append({"gem": gem, "property": props})
        return res

def select_gems(id):
    with Session(engine) as session:
        stats = select(Gem,).where(Gem.id == id)
        result = session.exec(stats)
        return result.first()
        
if __name__ == "__main__":
    pass