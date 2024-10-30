# JWT = Json Web Token , see jwt.io

# ===============================================
# Source with full explanation of the flow:
# https://www.youtube.com/watch?v=SKPms69KIco
# ===============================================

from datetime import datetime, timedelta
from fastapi import APIRouter, Depends, status
from fastapi.exceptions import HTTPException
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from jose import jwt, JWTError
from passlib.context import CryptContext
from pydantic import BaseModel

router = APIRouter()


SECRET_KEY = 'LongSSLStringAccordingToALLSecurityBestPractices'
ALGORITHM = 'HS256'
ACCESS_TOKEN_EXPIRE_MINUTES = 30

fake_users_db = dict(
    johndoe=dict(
        username='johndoe',
        email='johndoe@example.com',
        full_name='John Doe',
        disabled=False,
        # to get the hash, execute in console:
        # python
        # >> from passlib.context import CryptContext
        # >> pwd_context = CryptContext(schemes=['bcrypt'], deprecated='auto')
        # >> pwd_context.hash('your psw here')
        hashed_password='$2b$12$7G3NUo52zkrUocpDEaI7A.IkW5hBEXWrWwk/IRAJe68vVqDOLHJp6',
    )
)


class Token(BaseModel):
    access_token: str


class TokenData(BaseModel):
    username: str | None = None


class User(BaseModel):
    username: str
    email: str | None = None
    full_name: str | None = None
    disabled: bool = False


class UserInDB(User):
    hashed_password: str


# docs here: https://passlib.readthedocs.io/en/stable/lib/passlib.context.html
pwd_context = CryptContext(schemes=['bcrypt'], deprecated='auto')

oauth2_scheme = OAuth2PasswordBearer(tokenUrl='tokenlocation')


def verify_password(plain_password, hashed_password):
    return pwd_context.verify(plain_password, hashed_password)


def get_password_hash(password):
    return pwd_context.hash(password)


def get_user(db, username: str):
    if username in db:
        user_dict = db[username]
        return UserInDB(**user_dict)


def authenticate_user(fake_db, username: str, password: str):
    user = get_user(fake_db, username)

    if not user:
        return False

    if not verify_password(password, user.hashed_password):
        return False

    return user


def create_access_token(data: dict, expires_delta: timedelta | None = None ):
    to_encode = data.copy()
    if expires_delta:
        expire = datetime.now() + expires_delta
    else:
        expire = datetime.now() + timedelta(minutes=15)

    to_encode.update({'exp': expire})
    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
    return encoded_jwt


@router.post('/tokenlocation', response_model=Token)
async def login_for_access_token(form_data: OAuth2PasswordRequestForm = Depends()):
    user = authenticate_user(fake_users_db, form_data.username, form_data.password)

    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail='Incorrect username or password',
            header={'WWW-Authenticate': 'Bearer'},
        )

    access_token_expires = timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    access_token = create_access_token(data={'sub': user.username}, expires_delta=access_token_expires)

    return {'access_token': access_token, 'token_type': 'bearer'}


async def get_current_user(token: str = Depends(oauth2_scheme)):
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail = 'Could not validate the credentials',
        header = {'WWW-Authenticate': 'Bearer'}
    )

    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
    except JWTError:
        raise credentials_exception
    else:
        username: str = payload.get('sub')

    if username is None:
        raise credentials_exception
    
    token_data = TokenData(username=username)
    user = get_user(fake_users_db, username = token_data.username)

    if user is None:
        raise credentials_exception
    
    return user
    

async def get_current_active_user(current_user: User = Depends(get_current_user)):
    if current_user.disabled:
        raise HTTPException(status_code=400, detail = 'Inactive user')

    return current_user   


@router.get('/jwt_user/me', response_model=User)
async def get_me(current_user: User = Depends(get_current_active_user)):
    return current_user

@router.get('/jwt_users/me/items')
async def get_me(current_user: User = Depends(get_current_active_user)):
    return [{'item_id': 'foo', 'owner': current_user.username}]