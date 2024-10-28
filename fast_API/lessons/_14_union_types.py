from fastapi import APIRouter
from pydantic import BaseModel
from typing import Literal, Union

router = APIRouter()


class BaseItem(BaseModel):
    descr: str
    type: str


class CarItem(BaseItem):
    type: str = 'car'


class PlaneItem(BaseItem):
    type: str = 'plane'
    size: int


items = {
    'item1': {'descr': 'This is a car', 'type': 'car'},
    'item2': {'descr': 'This is a plane', 'type': 'plane', 'size': 5},
}


@router.get('/metal_items/{item_id}', response_model=Union[PlaneItem, CarItem])
async def get_some_metal(item_id: Literal['item1', 'item2']):

    return items[item_id]

