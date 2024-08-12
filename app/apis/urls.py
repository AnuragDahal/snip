from fastapi import APIRouter,status,Query
from starlette.responses import RedirectResponse
from ..core.database import urls_collection
from pydantic import HttpUrl
from ..handlers.Url.urlhandler import HandleUrl
from ..handlers.exception import ErrorHandler

router= APIRouter(tags=["URL"])

@router.post("/shorten",status_code=status.HTTP_201_CREATED)
async def shorten_url(long_url: HttpUrl=Query(...)):
    """
    Shorten the long url to a short url
    """
    
    short_url=await HandleUrl.HandleUrlShortening(long_url)
    return short_url


@router.get("/{short_url}")
async def redirect_to_long_url(short_url: str):
    """
    Redirect to the long URL based on the short URL
    """
    result = await HandleUrl.HandleUrlRedirection(short_url)
    if "long_url" in result:
        return RedirectResponse(url=result["long_url"])
    else:
        return ErrorHandler.NotFound("Url does not exists or is invalid")
    