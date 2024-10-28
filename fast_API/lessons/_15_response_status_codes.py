from fastapi import APIRouter, status

router = APIRouter()


@router.post('/status_code', status_code=201)  # overrides HTML code 200
async def return_code(name: str):

    return {'name': name}


@router.delete('/items/{pk}', status_code=204)  # 204 is "No content"
async def delete_item(pk: str):
    print('pk is: ', pk)

    return pk  # returns pk in front end and HTML code 204 in the back


@router.get('/moved_items', status_code=status.HTTP_301_MOVED_PERMANENTLY)
async def get_moved_items():

    return {'nothing': 'here'}  # returns json in front end, 301 in the back
