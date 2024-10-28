from fastapi import APIRouter, Body
from pydantic import BaseModel, Field

router = APIRouter()


class Item(BaseModel):
    name: str
    desc: str | None = None
    price: float
    tax: float | None = None

    # this will show up as an example in docs
    class Config:
        json_schema_extra = {
            'example': {
                'name': 'foo',
                'desc': 'very nice item',
                'price': 16.9,
                'tax': 1.2,
            }
        }


# examples for individual fields
class User(BaseModel):
    name: str = Field(..., example='Bob')  # example will be "Bob"
    age: int = Field(..., ge=18)  # example will be 18 (because the defualt 0 zero is invalid)
    guild: str | None = None  # example will be "string"
    points: int  # example will be 0


class Cat(BaseModel):
    name: str
    color: str


@router.put('/nice_item/{item_id}')
async def update_item(item_id: int, item: Item):
    results = {'item_id': item_id, 'item': item}

    return results


@router.put('/nice_user/{user_id}')
async def update_user(user_id: int, user: User):
    results = {'user_id': user_id, 'user': User}

    return results


@router.put('/this_is_cats/{cat_id}')
async def look_at_this_cat(
    cat_id: int,
    # defining example data inline
    cat: Cat = Body(..., example={'name': 'Snowball', 'color': 'black'}),
):

    results = {'cat_id': cat_id, 'cat': cat}

    return results


@router.put('/multiple_example_cats/{cat_id}')
async def not_a_dog(
    cat_id: int,
    # defining multiple examples  inline
    cat: Cat = Body(
        ...,
        openapi_examples={
            'normal': {
                'name': 'Snowball',
                'color': 'black',
            },
            'converted': {
                'summary': 'This is another example cat',
                'description': 'This is definitelly not a dog',
                'value': {'name': 'Rex', 'color': 'grey'},
            },
            'invalid': {
                'summary': 'This is a dog',
                'value': {'name': 'Fido', 'color': 'white'},
            },
        },
    ),
):

    results = {'cat_id': cat_id, 'cat': cat}

    return results
