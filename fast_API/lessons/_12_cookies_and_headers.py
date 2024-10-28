from fastapi import APIRouter, Cookie, Header

router = APIRouter()


@router.get('/cookies')
async def get_cookies(
    cookie_id: str | None = Cookie(None),
    accept_encoding: str | None = Header(None),
    sec_ch_ua: str | None = Header(None),
    user_agent: str | None = Header(None),
    x_token: list[str] | None = Header(None),
):

    return {
        'cookie': cookie_id,
        'Accept-Encoding': accept_encoding,
        'sec-ch-ua': sec_ch_ua,
        'User-Agent': user_agent,
        'X-Token values': x_token,
    }
