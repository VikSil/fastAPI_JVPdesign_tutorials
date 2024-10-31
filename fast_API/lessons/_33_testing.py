from fastapi import APIRouter, Header
from fastapi.exceptions import HTTPException
from pydantic import BaseModel

router = APIRouter()

fake_secret_token = 'coneofsilence'
fake_db = dict(
    foo=dict(id='foo', title='Foo', description='FooFoo, the white poodle'),
    bar=dict(id='bar', title='Bar', description='Bartender'),
)


class Item(BaseModel):
    id: str
    title: str
    description: str | None = None


@router.get('/testing_items/{item_id}', response_model=Item)
async def read_main(item_id: str, x_token: str = Header(...)):
    if x_token != 'coneofsilence':
        raise HTTPException(status_code=400, detail='Invalid X-Token header')

    if item_id not in fake_db:
        raise HTTPException(status_code=404, detail='Item not found')

    return fake_db[item_id]


@router.post('/testing_items', response_model=Item)
async def create_item(item: Item, x_token: str = Header(...)):
    if x_token != 'coneofsilence':
        raise HTTPException(status_code=400, detail='Invalid X-Token header')

    if item.id in fake_db:
        raise HTTPException(status_code=400, detail='Item already exists')

    fake_db[item.id] = item

    return item
