from enum import Enum
from fastapi import FastAPI

app = FastAPI()


# GET, POST, PUT requests

@app.get('/', description = 'This is our first route', deprecated = True)
async def base_get_route():
    return{'message': 'Hello, everyone!'}

@app.post("/")
async def post():
    return {'message':'hello from the post route'}

@app.put('/')
async def put():
    return {'message': 'hello from the put route'}

# Route priority

@app.get('/users')
async def list_users():
    return {'message':'list users route'}


@app.get('/users/me')
async def get_current_user():
    return {'message': 'this is the curent user'}


# Path parameters

@app.get('/users/{user_id}')
async def get_user(user_id: str):
    return {'user_id': user_id}


class FoodEnum(str, Enum):
    fruits = 'fruits'
    veg = 'veg'
    nuts = 'nuts'

@app.get('/foods/{food_name}')
async def get_food(food_name: FoodEnum):
    if food_name == FoodEnum.veg:
        return {'food name': food_name, 'message': 'good choice'}
    
    if food_name.value  == 'fruits':
        return {'food_name': food_name, 'message':'tasty'}
    
    return {'food_name': food_name, 'message': 'this is nuts'}