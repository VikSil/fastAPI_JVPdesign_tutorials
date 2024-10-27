from enum import Enum
from fastapi import FastAPI
from typing import Optional

app = FastAPI()


# GET, POST, PUT requests


@app.get('/', description='This is our first route', deprecated=True)
async def base_get_route():
    return {'message': 'Hello, everyone!'}


@app.post("/")
async def post():
    return {'message': 'hello from the post route'}


@app.put('/')
async def put():
    return {'message': 'hello from the put route'}


# Route priority


@app.get('/users')
async def list_users():
    return {'message': 'list users route'}


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

    if food_name.value == 'fruits':
        return {'food_name': food_name, 'message': 'tasty'}

    return {'food_name': food_name, 'message': 'this is nuts'}


# Query parameters

fake_items_db = [{'item_name': 'foo'}, {'item_name': 'bar'}, {'item_name': 'baz'}]


@app.get('/items')
async def list_items(skip: int = 0, limit: int = 10):
    return fake_items_db[skip : skip + limit]


@app.get('/items/{item_id}')
async def get_item(item_id: str, q: Optional[str] = None):  # q: str | None = None
    if q:
        return {'item_id': item_id, q: q}
    return {'item_id': item_id}


@app.get('/inventory')
async def get_something(required_query: str):
    message = f'Here is your item: {required_query}'
    return {'item': message}


# Type conversion

# bool in the URL will convert from 1, true, on, yes - all case insenitive
@app.get('/users/{user_id}/items/{item_id}')
async def get_user_item(user_id: int, item_id: str, required_q: str, q: str | None = None, short: bool = False):
    item = {'item_id': item_id, 'owner_id': user_id, 'origin': required_q}
    if q:
        item.update({'q': q})  # update is append not override
    if not short:
        item.update({'description': 'Lorem ipsum dolor sit'})

    return item
