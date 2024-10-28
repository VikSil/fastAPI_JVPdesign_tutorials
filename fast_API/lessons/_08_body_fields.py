from fastapi import APIRouter, Body
from pydantic import BaseModel, Field

router = APIRouter()


# using Field adds details to the documentation
class Item(BaseModel):
    name: str
    desc: str | None = Field(None, title='description of the item', max_length=200)
    price: float = Field(..., gt=0, description='Must be greater than zero')
    tax: float | None = None


@router.put('/it_is_an_item/{item_id}')
async def update_item(item_id: int, item: Item = Body(..., embed=True)):

    results = {'item_id': item_id, 'item': item}

    return results
