# ===============================================
# Source with full explanation of the flow:
# https://www.youtube.com/watch?v=B5AMPx9Z1OQ
# ===============================================

from fastapi import APIRouter, Depends, status
from fastapi.exceptions import HTTPException
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from pydantic import BaseModel

router = APIRouter()

# OAuth2 requires python-multipart package to be installed
oath2_scheme = OAuth2PasswordBearer(tokenUrl='tokenroute')


@router.get('/secure_items')
# including OAuth2 scheme will cause an Authorise button at the top of the docs
async def read_items(token: str = Depends(oath2_scheme)):
    return {'token': token}


fake_users_db = {
    'johndoe': dict(
        username='johndoe',
        email='johndoe@example.com',
        full_name='John Doe',
        disabled=False,
        hashed_password='fakehashedsecret',
    ),
    'alice': dict(
        username='alice',
        email='alice@example.com',
        full_name='Alice Wonder',
        disabled=True,
        hashed_password='fakehashedsecret2',
    ),
}


def fake_hash_password(password: str):
    return f'fakehashed{password}'


class User(BaseModel):
    username: str
    email: str | None = None
    full_name: str | None = None
    disabled: bool | None = None


class UserInDB(User):
    hashed_password: str


def get_user(db, username: str):
    if username in db:
        user_dict = db[username]
        return UserInDB(**user_dict)


def fake_decode_token(token):
    return get_user(fake_users_db, token)


async def get_current_user(token: str = Depends(oath2_scheme)):
    user = fake_decode_token(token)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail='Invalid authentication credentials',
            headers={'WWW-Authenticate': 'Bearer'},
        )

    return user


async def get_current_active_user(current_user: User = Depends(get_current_user)):
    if current_user.disabled:
        raise HTTPException(status_code=400, detail='Inactive user')

    return current_user


@router.post('/tokenroute')  # url has to match the one of OAuth2PasswordBearer instance
async def login(form_data: OAuth2PasswordRequestForm = Depends()):
    user_dict = fake_users_db.get(form_data.username)
    if not user_dict:
        raise HTTPException(status_code=400, detail='Incorrect password or username')

    user = UserInDB(**user_dict)
    hashed_password = fake_hash_password(form_data.password)
    if not hashed_password == user.hashed_password:
        print(hashed_password)
        print(user.hashed_password)
        raise HTTPException(status_code=400, detail='Incorrect username or password')

    return {'access_token': user.username, 'token_type': 'bearer'}


@router.get('/tokenised_users/me')
async def get_me(current_user: User = Depends(get_current_active_user)):

    return current_user
