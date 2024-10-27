from enum import Enum
from fastapi import FastAPI, Query, Path
from pydantic import BaseModel
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


@app.get('/item_validation/{item_id}')
async def read_item_validation(
    *,  # makes everything that follows a kwarg
    # Path allows to validate path variables
    item_id: int = Path(..., title='the ID of the item', ge=10),  # ge = greater-or-equal
    q: str,  # now it is a required kwarg and can follow assigned arguments without having a value itself
):

    result = {'item_id': item_id}

    if q:
        result.update({'q': q})

    return result


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


@app.get('/lux_items')
async def read_items(
    q1: str | None = Query(None, min_length=3, max_length=10),
    q2: str = Query('default_value', regex='^\w+$'),
    q3: list[str] | None = Query(['default', 'for a ', 'query', 'with', 'multiple', 'values']),
):
    results = {'items': [{'item_id': 'foo'}, {'item_id': 'bar'}], 'q2': q2}

    if q1:
        results.update({'q1': q1})

    return results


@app.get('/more_items')
async def more_items(required_validated_query_with_no_default_value: str = Query(..., min_length=3, max_length=10)):

    results = {'items': [{'item_id': 'foo'}, {'item_id': 'bar'}], 'q': required_validated_query_with_no_default_value}

    return results


@app.get('/metadata')
async def metadata(
    q: str | None = Query(
        None,
        min_length=3,
        max_length=10,
        title='Query with metadata',
        desc='This is a query with some metadata',
        depricated=True,
        alias='url-slug-with-dashes',
    )
):

    results = {'items': [{'item_id': 'foo'}, {'item_id': 'bar'}], 'q': q}

    return results


@app.get('/hidden_items')
async def hidden_query(hidden_query: str | None = Query(None, include_in_schema=False)):
    if hidden_query:
        return {'hidden_query': hidden_query}

    return {'hidden_query': 'Not found'}


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


# Request body


class Item(BaseModel):
    name: str
    description: Optional[str] = None
    price: float
    tax: int | None = None  # python 3.10+


@app.post('/items')
async def create_item(item: Item):
    item_dict = item.model_dump()  # previously .dict()

    if item.tax:
        price_with_tax = item.price + item.tax
        item_dict.update({'price_with_tax': price_with_tax})

    return item_dict


@app.put('/items/{item_id}')
async def create_item_with_id(item_id: int, item: Item, q: str | None = None):
    result = {'item_id': item_id, **item.model_dump()}
    if q:
        result.update({'q': q})

    return result
