from enum import Enum
from functools import wraps

from config import Config

from persistency.connection import get_db
from persistency.connection_for_test_db import get_test_db


class QueryResponseOptions(str, Enum):
    All = "all"
    First = "first"


class ReadDatabaseSession:
    def __init__(
        self, query_type: QueryResponseOptions = QueryResponseOptions.All
    ):
        self.query_type = query_type

    def __call__(self, function):
        async def wrapper(*args, **kwargs):
            db = get_db if Config.production_mode else get_test_db
            async with await db() as session:
                # Call original function
                query = await function(*args, **kwargs)

                # Execute query
                result = await session.execute(query)

                if self.query_type == QueryResponseOptions.First:
                    return result.scalars().first()

                return result.scalars().all()

        return wrapper


class WriteDatabaseSession:
    def __init__(self, function):
        self.function = function
        wraps(function)(self)

    async def __call__(self, *args, **kwargs):
        db = get_db if Config.production_mode else get_test_db
        async with await db() as session:
            # Call original function
            query = await self.function(*args, **kwargs)

            result = await session.execute(query)

            await session.commit()

            return result
