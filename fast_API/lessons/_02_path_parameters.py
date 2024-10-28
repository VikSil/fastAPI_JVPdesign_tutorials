from enum import Enum
from fastapi import APIRouter, Path

router = APIRouter()

# Path parameters


@router.get('/users/{user_id}')
async def get_user(user_id: str):
    return {'user_id': user_id}


class FoodEnum(str, Enum):
    fruits = 'fruits'
    veg = 'veg'
    nuts = 'nuts'


@router.get('/foods/{food_name}')
async def get_food(food_name: FoodEnum):
    if food_name == FoodEnum.veg:
        return {'food name': food_name, 'message': 'good choice'}

    if food_name.value == 'fruits':
        return {'food_name': food_name, 'message': 'tasty'}

    return {'food_name': food_name, 'message': 'this is nuts'}


@router.get('/item_validation/{item_id}')
async def read_item_validation(
    *,  # makes everything that follows a kwarg
    # Path allows to validate path variables
    item_id: int = Path(..., title='the ID of the item', ge=10),  # ge = greater-or-equal
    q: str,  # now it is a required kwarg and can follow assigned arguments without having a value itself
):

    result = {'item_id': item_id}

    if q:
        result.update({'q': q})

    return result
