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


@router.post('/response_model_items')  # response model will be "string"
async def create_item(item: Item):

    return item


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


# ==========================================================


class ListItem(BaseModel):
    name: str
    descr: str


list_items = [
    {'name': 'foo', 'descr': 'this is foo'},
    {'name': 'bar', 'descr': 'this is bar'},
]


@router.get('/another_list_of_items', response_model=list[ListItem])
async def read_items():

    return list_items


@router.get('/custom_response', response_model=dict[str, float])
async def get_arbitrary():
    return {'foo': 1, 'bar': '2'}


# ==========================================================


class UserBase(BaseModel):
    username: str
    email: EmailStr
    full_name: str | None = None


class UserIn(UserBase):
    password: str


class UserOut(UserBase):
    pass  # same as UserBase model, no additional atributes


class UserInDB(UserBase):
    hashed_password: str


def fake_psw_hasher(raw_psw: str):
    return f'supersecret{raw_psw}'


def fake_save_user(user_in: UserIn):
    hashed_psw = fake_psw_hasher(user_in.password)

    # model_dump converts an object to a dict
    # double star spreads a dictionary into class atributes
    user_in_db = UserInDB(**user_in.model_dump(), hashed_password=hashed_psw)
    print('user_in.model_dump() is: ', user_in.model_dump())
    print("Let's pretend that the User was saved to DB")

    return user_in_db


@router.post('/fake_user', response_model=UserOut)  # adds the response model to docs
async def create_user(user_in: UserIn):
    user_saved = fake_save_user(user_in)
    print(user_saved)  # this will contain the hashed password
    return user_saved  # this will not because the response model does not have a password
