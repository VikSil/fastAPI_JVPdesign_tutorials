from fastapi import APIRouter
from pydantic import BaseModel, EmailStr
from typing import Literal

router = APIRouter()


class Item(BaseModel):
    name: str
    descr: str | None = None
    price: float
    tax: float = 5.2
    tags: list[str] = []


stuff = {
    'foo': {'name': 'foo', 'price': 20},
    'bar': {'name': 'bar', 'description': 'bartender', 'tax': 20, 'price': 20},
    'baz': {'name': 'baz', 'description': None, 'tax': 9.5, 'price': 4, 'tags': []},
}


class UserBase(BaseModel):
    username: str
    email: EmailStr
    full_name: str | None = None


class UserIn(UserBase):
    psw: str


# this has no psw, so it does not get exposed
class UserOut(UserBase):
    pass


@router.post('/response_model_items')  # response model will be "string"
async def create_item(item: Item):

    return item


@router.post('/user_in', response_model=UserOut)  # adds the response model to docs
async def create_user(user: UserIn):
    return user


# dont show a property in the response, unless the object has that property
@router.get('/stuff/{stuff_id}', response_model=Item, response_model_exclude_unset=True)
async def get_stuff(item_id: Literal['foo', 'bar', 'baz']):  # restricts the docs query options

    return stuff[item_id]


# show set properties in the response and
# if object does not have name or description, use default values in the response
@router.get('/named_items/{item_id}/name', response_model=Item, response_model_include={'name', 'descr'})
async def read_item_name(item_id: Literal['foo', 'bar', 'baz']):
    return stuff[item_id]


# always exclude tax property from the response model
@router.get('/named_items/{item_id}/public', response_model=Item, response_model_exclude={'tax'})
async def read_item_data(item_id: Literal['foo', 'bar', 'baz']):
    return stuff[item_id]
