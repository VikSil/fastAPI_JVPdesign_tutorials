from fastapi import APIRouter, Depends


router = APIRouter()


async def common_parameters(q: str | None = None, skip: int = 0, limit: int = 100):

    return {'q': q, 'skip': skip, 'limit': limit}


@router.get('/dry_items')
async def read_items(commons: dict = Depends(common_parameters)):

    return commons


@router.get('/dry_users')
async def read_items(commons: dict = Depends(common_parameters)):

    return commons
