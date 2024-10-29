from fastapi import APIRouter, Body, Form
from pydantic import BaseModel

router = APIRouter()


@router.post('/login')
# payload will be a form
async def login(username: str = Form(...), password: str = Form(...)):

    print('password is: ', password)
    return {'username': username}


@router.post('/login_still_form')
# if inputs are mixed, then payload will be a form
async def login(username: str = Form(...), password: str = Body(...)):

    print('password is: ', password)
    return {'username': username}


class User(BaseModel):
    username: str
    password: str


@router.post('/login_json')
async def login_json(user: User):  # payload will be a json object

    return user


@router.post('/login_also_json')
# if all inputs are in the request body, then payload will be a json object
async def login_also_json(username: str = Body(...), password: str = Body(...)):

    return {'username': username}
