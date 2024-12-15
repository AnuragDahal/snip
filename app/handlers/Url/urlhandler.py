from ...core.database import urls_collection
from pydantic import HttpUrl
from ..exception import ErrorHandler
import secrets
import string
from ...utils.envutils import Environment
import dns.resolver
from fastapi import HTTPException
import asyncio
from functools import partial

env = Environment()


class HandleUrl:
    @staticmethod
    def generate_unique_string():
        alphabet = string.ascii_letters + string.digits
        shorted_string = ''.join(secrets.choice(alphabet) for _ in range(8))
        return shorted_string

    @staticmethod
    async def check_domain(domain: str):
        """
        Perform DNS lookup using dns.resolver instead of aiodns
        """
        try:
            # Run DNS query in a thread pool to avoid blocking
            loop = asyncio.get_running_loop()
            resolver = dns.resolver.Resolver()
            # Set a timeout to avoid hanging
            resolver.timeout = 3
            resolver.lifetime = 3

            # Run the DNS query in a thread pool
            await loop.run_in_executor(
                None,
                partial(resolver.resolve, domain, 'A')
            )
            return True
        except Exception:
            raise HTTPException(
                status_code=404,
                detail="Domain does not exist or is unreachable"
            )

    @staticmethod
    async def HandleUrlShortening(url: HttpUrl):
        """
        Shorten the long URL to a short URL.
        """
        try:
            domain = url.host

            # Check domain existence
            await HandleUrl.check_domain(domain)

            # Generate unique string
            unique_strings = HandleUrl.generate_unique_string()

            # MongoDB operation
            new_url = await urls_collection.insert_one({
                "long_url": str(url),
                "short_url": unique_strings
            })

            return {
                "short_url": f"{env.DOMAIN}{unique_strings}"
            }
        except HTTPException as he:
            raise he
        except Exception as e:
            return ErrorHandler.Forbidden(str(e))

    @staticmethod
    async def HandleUrlRedirection(unique_string: str):
        """
        Redirect to the long url
        """
        try:
            url = await urls_collection.find_one({"short_url": unique_string})
            if url:
                return {"long_url": url["long_url"]}
            return ErrorHandler.NotFound("Url does not exists or is invalid")
        except Exception as e:
            return ErrorHandler.Error(str(e))
