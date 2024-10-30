from fastapi import APIRouter, Depends


router = APIRouter()


fake_items_db = [
    {'item_name': 'Foo'},
    {'item_name': 'Bar'},
    {'item_name': 'Baz'},
]


class CommonQueryparams:
    def __init__(self, item_id: int, q: str | None = None, skip: int = 0, limit: int = 100):
        self.q = q
        self.skip = skip
        self.limit = limit
        self.item_id = item_id


@router.get('/common_items/{item_id}')  # this path variable will also be passed into the commons object
# will expect inputs to be the same as the init inputs for the depended class
async def read_items(commons: CommonQueryparams = Depends(CommonQueryparams)):  # type annotation can be omitted
    response = {}

    print(commons.item_id)

    if commons.q:
        response.update({'q': commons.q})

    items = fake_items_db[commons.skip : commons.skip + commons.limit]  # this is a slice
    response.update({'items': items})

    return response
