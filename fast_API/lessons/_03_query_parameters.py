from fastapi import APIRouter, Query
from typing import Optional

router = APIRouter()

# Query parameters

fake_items_db = [{'item_name': 'foo'}, {'item_name': 'bar'}, {'item_name': 'baz'}]


@router.get('/items')
async def list_items(skip: int = 0, limit: int = 10):
    return fake_items_db[skip : skip + limit]


@router.get('/items/{item_id}')
async def get_item(item_id: str, q: Optional[str] = None):  # q: str | None = None
    if q:
        return {'item_id': item_id, q: q}
    return {'item_id': item_id}


@router.get('/inventory')
async def get_something(required_query: str):
    message = f'Here is your item: {required_query}'
    return {'item': message}


@router.get('/lux_items')
async def read_items(
    q1: str | None = Query(None, min_length=3, max_length=10),
    q2: str = Query('default_value', regex='^\w+$'),
    q3: list[str] | None = Query(['default', 'for a ', 'query', 'with', 'multiple', 'values']),
):
    results = {'items': [{'item_id': 'foo'}, {'item_id': 'bar'}], 'q2': q2}

    if q1:
        results.update({'q1': q1})

    return results


@router.get('/more_items')
async def more_items(required_validated_query_with_no_default_value: str = Query(..., min_length=3, max_length=10)):

    results = {'items': [{'item_id': 'foo'}, {'item_id': 'bar'}], 'q': required_validated_query_with_no_default_value}

    return results


@router.get('/metadata')
async def metadata(
    q: str | None = Query(
        None,
        min_length=3,
        max_length=10,
        title='Query with metadata',
        desc='This is a query with some metadata',
        depricated=True,
        alias='url-slug-with-dashes',
    )
):

    results = {'items': [{'item_id': 'foo'}, {'item_id': 'bar'}], 'q': q}

    return results


@router.get('/hidden_items')
async def hidden_query(hidden_query: str | None = Query(None, include_in_schema=False)):
    if hidden_query:
        return {'hidden_query': hidden_query}

    return {'hidden_query': 'Not found'}
