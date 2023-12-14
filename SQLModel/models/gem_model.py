from sqlmodel import SQLModel, Field, Relationship
from typing import Optional, List, Any
from enum import Enum
import random

    
class Enum_lst(Enum):
    @classmethod
    def gen_list(cls):
        return list(map(lambda c: c.value, cls))
    
class GemColor(Enum_lst):
    D = 'D'
    E = 'E'
    G = 'G' 
    F = 'F' 
    H = 'H'
    I = 'I'
    
    
class GemTypes(Enum_lst):
    Diamond = 'Diamond'
    Emerald = 'Emerald'
    Ruby = 'Ruby' 
    
    
class GemClarity(Enum_lst):
    SI = 1
    VS =  2
    VVS = 3
    FL = 4
    

class Gem(SQLModel, table=True):
    id: Optional[int] = Field(primary_key=True)
    price: float
    is_available: bool = True
    gem_type: GemTypes = GemTypes.Diamond 
    gem_properties_id: Optional[int] = Field(foreign_key='gemproperties.id')
    gem_properties: Optional['GemProperties'] = Relationship(back_populates='gem')


class GemProperties(SQLModel, table=True):
    id: Optional[int] = Field(primary_key=True)
    size: float = 1
    color: Optional[GemColor] = None
    clarity: Optional[GemClarity] = None
    gem: List[Gem] = Relationship(back_populates='gem_pros')
    
    
if __name__ == '__main__':
    gem_type = GemClarity.gen_list()
    print(gem_type)