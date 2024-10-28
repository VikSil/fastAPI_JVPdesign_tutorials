from fastapi import APIRouter

router = APIRouter()

# GET, POST, PUT requests


@router.get('/', description='This is our first route', deprecated=True)
async def base_get_route():
    return {'message': 'Hello, everyone!'}


@router.post("/")
async def post():
    return {'message': 'hello from the post route'}


@router.put('/')
async def put():
    return {'message': 'hello from the put route'}
