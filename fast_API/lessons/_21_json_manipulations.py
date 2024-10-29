from datetime import datetime
from fastapi import APIRouter
from fastapi.encoders import jsonable_encoder
from pydantic import BaseModel

router = APIRouter()


fake_db = {}


class Item(BaseModel):
    name: str | None = None
    title: str
    timestamp: datetime
    description: str | None = None


@router.put('/encoder_item/{id}')
async def update_item(id: str, item: Item):
    json_compatible_item_data = jsonable_encoder(item)
    fake_db[id] = json_compatible_item_data  # this makes all input data types compatible with DB types
    print(fake_db)

    return 'Success'


class FooBar(BaseModel):
    name: str
    description: str | None = None
    price: float | None = None
    tax: float = 10.5
    tags: list[str] = []


items = {
    'foo': {'name': 'Foo', 'price': 50.2},
    'bar': {'name': 'Bar', 'description': 'bartender', 'price': 62, 'tax': 20.2},
    'baz': {'name': 'Baz', 'description': None, 'price': 50.2, 'tax': 1.5, 'tags': []},
}


@router.get('/foobar_items/{item_id}', response_model=FooBar)
async def read_foobar(item_id: str):

    return items.get(item_id)


# replace all the data
@router.put('/foobar_items/{item_id}', response_model=FooBar)
async def update_item(item_id: str, item: FooBar):
    update_item_encoded = jsonable_encoder(item)
    items[item_id] = update_item_encoded

    return update_item_encoded


# only update the fields that are passed in
@router.patch('/foobar_items/{item_id}', response_model=FooBar)
async def patch_item(item_id: str, item: FooBar):
    stored_item_data = items.get(item_id)
    print(stored_item_data)
    if stored_item_data is not None:
        stored_item_model = FooBar(**stored_item_data)  # spread object as a json
    else:
        stored_item_model = FooBar()
    update_data = item.model_dump(exclude_unset=True)  # jsonify the request body and ignore defaults
    updated_item = stored_item_model.model_copy(update=update_data)
    items[item_id] = jsonable_encoder(updated_item)

    return updated_item
