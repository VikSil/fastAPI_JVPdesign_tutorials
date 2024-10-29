from enum import Enum
from fastapi import APIRouter, status
from pydantic import BaseModel

router = APIRouter()


class Item(BaseModel):
    name: str
    description: str | None = None
    price: float
    tax: float | None = None
    tags: set[str] = set()


class Tags(Enum):
    items = 'items'
    users = 'users'


# tags organise docs into chapters
@router.post(
    '/path_items',
    response_model=Item,
    status_code=status.HTTP_201_CREATED,
    tags=['items'],
    summary='create an item',  # shows up instead of the function name in the docs
    # shows at the top of the route card in the docs
    description='create an item with a name, description, price, tax and tags',
    response_description='The description that will show up at the top of the response in the docs',
)
async def create_item(item: Item):

    return item


@router.get('/path_items', tags=[Tags.items])
async def read_items():
    """
    This is a docstring. It will be displayed at the very top of the route card in the docs.

    - and **this** is a docstring
    - being _interpreted_ as a markdown
    """
    return [{'name': 'foo', 'price': 42}]


@router.get('/path_users', tags=[Tags.users, 'users'])  # this will show up under both tags
async def read_users():
    return [{'username': 'janeDoe'}]


# depricated endpoint will still work, but it is greyed out in the docs
@router.get('/elements', tags=[Tags.items], deprecated=True)
async def read_elements():

    return [{'item_id': 'foo'}]
