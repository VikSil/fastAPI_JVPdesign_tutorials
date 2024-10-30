from fastapi import APIRouter, Body, Depends


router = APIRouter()


def query_extractor(q: str | None = None):
    return q


# uses query_extractor to determine the value of q
def query_or_body_extractor(q: str = Depends(query_extractor), last_query: str | None = Body(None)):

    if q:
        return q

    return last_query


@router.post('/subquery_item')
# uses query_or_body_extractor to determine the value of query_or_body
# hence, needs the same inputs as query_or_body_extractor
# and assigns a value to query_or_body by executing query_or_body_extractor
async def try_query(query_or_body: str = Depends(query_or_body_extractor)):

    return {'q or body': query_or_body}
