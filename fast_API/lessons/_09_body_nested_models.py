from fastapi import APIRouter, Body
from pydantic import BaseModel, Field, HttpUrl

router = APIRouter()


class Image(BaseModel):
    url: HttpUrl  # adds validation for a URL string (with http(s)://)
    name: str


class Item(BaseModel):
    name: str
    desc: str | None = None
    price: float
    tax: float | None = None
    taglist: list[int] = []  # will expect a list of ints or smthn that can be converted to int
    tagset: set[str] = set()  # will keep unique values only
    image: Image | None = None  # nested dictionary/model (optional)
    images: list[Image] | None = None  # list of image dictionaries (optional)


class Offer(BaseModel):
    name: str
    description: str | None = None
    price: float
    items: list[Item]  # a list of items, which in turn have a list of images


@router.put('/items_again/{item_id}')
async def update_item(item_id: int, item: Item):

    results = {'item_id': item_id, 'item': item}

    return results


@router.post('/offers')
async def create_offer(offer: Offer = Body(..., embed=True)):  # will expect body to be a dict
    return offer


@router.post('/multi_images')
async def create_multiple_images(images: list[Image]):
    return images  # will expect the request body to be a list, not a dict


@router.post('/blah')
# will expect the body to be a dict with str keys parsable as ints and values parsable as floats
async def create_some_blahs(blahs: dict[int, float]):
    return blahs
