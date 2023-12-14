import string
import random
from models.gem_model import * 
from sqlmodel import Session
# from main import engine 

colors = string.ascii_uppercase[3:9]

color_multiplier = {
    'D': 1.8,
    'E': 1.6,
    'G': 1.4,
    'F': 1.2,
    'H': 1,
    'I': 0.8
}


def calculate_gem_price(gem, gem_pr):
    price = 1000
    if gem.gem_type == 'Ruby':
        price = 400
    elif gem.gem_type == 'Emerald':
        price = 650

    if gem_pr.clarity == 1:
        price *= 0.75
    elif gem_pr.clarity == 3:
        price *= 1.25
    elif gem_pr.clarity == 4:
        price *= 1.5

    price = price * (gem_pr.size**3)

    if gem.gem_type == 'Diamond':
        multiplier = color_multiplier[gem_pr.color]
        price *= multiplier

    return price


def create_gem_props():
    size = random.randint(3, 10)/10
    color = colors[random.randint(0, 5)]
    clarity = random.randint(1, 4)
    gem_p = GemProperties(size=size, color=color, clarity=clarity)
    print("=========================")
    print(gem_p)
    return gem_p

def create_gem(gem_p):
    gem = Gem(price=1000, gem_properties_id=gem_p.id)
    price = calculate_gem_price(gem, gem_p)
    gem.price = price
    return gem
    
    
def create_gem_db():
    gem_p = create_gem_props()
    # with Session(engine) as session:
    #     session.add(gem_p)
    #     session.commit()
    #     gem = create_gem(gem_p)
    #     session.add(gem)
    #     session.commit()
        
create_gem_db()