from fastapi import APIRouter

router = APIRouter()


@router.get('/users', tags=['users'])
async def read_users():
    return [{'username': 'Rick'}, {'username': 'morty'}]


@router.get('/users/me', tags=['users'])
async def read_user_me():
    return {'username': 'currentuser'}


@router.get('/user/{user_name}', tags=['users'])
async def read_user(username: str):
    return {'username': username}
