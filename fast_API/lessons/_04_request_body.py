from fastapi import APIRouter
from pydantic import BaseModel
from typing import Optional

router = APIRouter()

class Item(BaseModel):
    name: str
    description: Optional[str] = None
    price: float
    tax: int | None = None  # python 3.10+


@router.post('/items')
async def create_item(item: Item):
    item_dict = item.model_dump()  # previously .dict()

    if item.tax:
        price_with_tax = item.price + item.tax
        item_dict.update({'price_with_tax': price_with_tax})

    return item_dict


@router.put('/items/{item_id}')
async def create_item_with_id(item_id: int, item: Item, q: str | None = None):
    result = {'item_id': item_id, **item.model_dump()}
    if q:
        result.update({'q': q})

    return result
