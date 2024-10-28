from fastapi import APIRouter

router = APIRouter()


# Type conversion
# bool in the URL will convert from 1, true, on, yes - all case insenitive
@router.get('/users/{user_id}/items/{item_id}')
async def get_user_item(user_id: int, item_id: str, required_q: str, q: str | None = None, short: bool = False):
    item = {'item_id': item_id, 'owner_id': user_id, 'origin': required_q}
    if q:
        item.update({'q': q})  # update is append not override
    if not short:
        item.update({'description': 'Lorem ipsum dolor sit'})

    return item
