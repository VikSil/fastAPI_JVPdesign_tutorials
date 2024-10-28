from fastapi import APIRouter, Body, Path
from pydantic import BaseModel

router = APIRouter()


class Item(BaseModel):
    name: str
    description: str | None = None
    price: float
    tax: float | None = None


class User(BaseModel):
    username: str
    full_name: str | None = None


@router.put('/more_items/{item_id}')
async def update_item(
    *,
    item_id: int = Path(..., title='Id of the item to update', ge=0, lt=150),
    q: str | None = None,
    item: Item | None = None,
    user: User,
    importance: int = Body(...),  # makes it a body property not a query
):
    results = {'item_id': item_id}

    if q:
        results.upsate({'q': q})
    if item:
        results.upsate({'item': item})
    if user:
        results.update({'user': user})
    if importance:
        results.update({'importance': importance})

    return results


@router.put('dict_item/{item_id}')
async def make_item(
    *,
    item_id: int = Path(..., title='Id of the item to update', ge=0, lt=150),
    q: str | None = None,
    item: Item = Body(..., embed=True),  # item has to be passed in as a key to a dictionary of properties
):

    results = {'item_id': item_id}
    if q:
        results.upsate({'q': q})
    if item:
        results.upsate({'item': item})

    return results
