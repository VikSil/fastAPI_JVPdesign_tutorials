from datetime import datetime, time, timedelta
from fastapi import APIRouter, Body
from uuid import UUID

router = APIRouter()

# docs here:
# https://docs.pydantic.dev/1.10/usage/types/


@router.put('/items_no_kidding/{item_id}')
async def read_items(
    item_id: UUID,
    start_date: datetime | None = Body(None),
    end_date: datetime | None = Body(None),
    repeat_at: time | None = Body(None),
    process_after: timedelta | None = Body(None),
):

    start_process = start_date + process_after
    duration = end_date - start_process

    return {
        'item_id': item_id,
        'start_date': start_date,
        'end_date': end_date,
        'repeat': repeat_at,
        'process_after': process_after,
        'duration': duration,
    }
