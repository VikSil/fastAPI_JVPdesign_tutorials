from fastapi import APIRouter, Header, Depends
from fastapi.exceptions import HTTPException

router = APIRouter()


async def verify_token(x_token: str = Header(...)):

    if x_token != 'fake-super-secret-token':
        raise HTTPException(status_code=400, detail='X-Token header invalid')

    return 'hello'


@router.get('/token_items')
# will expect "fake-super-secret-token" as input and assign value to blah accordingly
async def read_items(blah: str = Depends(verify_token)):

    return [{'item': 'Foo'}, {'item': 'Bar'}, {'blah': blah}]


async def verify_key(x_key: str = Header(...)):
    if x_key != 'fake-super-secret-key':
        raise HTTPException(status_code=400, detail='X-Key header invalid')

    return x_key


# putting dependency in the decorator prohibits the use of the return value of that function
@router.get('/key_items', dependencies=[Depends(verify_token), Depends(verify_key)])
async def read_items():  # will require the header inputs it depends upon even though not declared here

    return [{'item': 'Foo'}, {'item': 'Bar'}]


# Global dependencies
# works for a FastAPI() object too
router = APIRouter(dependencies=[Depends(verify_token), Depends(verify_key)])


# will work the same way as /key_items, since the same dependencies
@router.get('/token_users')
async def read_users():
    return [{'username': 'Rick'}, {'username': 'Morty'}]
