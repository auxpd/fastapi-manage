from typing import Tuple

from fastapi import FastAPI
from ratelimit import RateLimitMiddleware, Rule
from ratelimit.auths import EmptyInformation
from ratelimit.backends.redis import RedisBackend

app = FastAPI()

rate_limit = RateLimitMiddleware(
    app,
)


async def AUTH_FUNCTION(scope: Scope) -> Tuple[str, str]:
    """
    Resolve the user's unique identifier and the user's group from ASGI SCOPE.

    If there is no user information, it should raise `EmptyInformation`.
    If there is no group information, it should return "default".
    """
    # FIXME
    # You must write the logic of this function yourself,
    # or use the function in the following document directly.
    return USER_UNIQUE_ID, GROUP_NAME