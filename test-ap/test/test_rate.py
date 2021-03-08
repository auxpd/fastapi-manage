import asyncio
from typing import Tuple

import aredis
import aioredis
from aredis.commands.strings import StringsCommandMixin
from aredis.client import mixins
from fastapi import FastAPI
# from ratelimit import RateLimitMiddleware, Rule
from ratelimit.backends.redis import RedisBackend
from ratelimit.auths.ip import client_ip
from ratelimit.types import Scope

from middleware.rate_limit import Rule, RateLimitMiddleware

app = FastAPI()


config = {
    r'^/hello': [Rule(minute=2, group="default"), Rule(group="admin")],
}

# rate_limit = RateLimitMiddleware(
#     app,
#     authenticate=auth_func,
#     backend=RedisBackend(password='Aa1234', db=12),
#     config=config,
# )

# rb = RedisBackend(password='Aa1234', db=12)
# app.add_middleware(RateLimitMiddleware,
#                    authenticate=auth_func,
#                    backend=rb,
#                    config=config,
#                    )
# 限流中间件
app.add_middleware(RateLimitMiddleware, config=config)


@app.on_event('startup')
async def startup():
    # await rb.is_blocking('Test1')
    # app.state.redis = aredis.StrictRedis(password='Aa1234', db=13)
    # await app.state.redis.get('A1')
    print('complete')


@app.get('/hello')
async def get():
    return 'test11'


if __name__ == '__main__':
    # loop = asyncio.get_event_loop()
    # loop.run_until_complete(main())
    import uvicorn

    uvicorn.run(app)
