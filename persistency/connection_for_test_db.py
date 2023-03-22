from config import Config
from sqlalchemy.ext.asyncio import AsyncSession, create_async_engine
from sqlalchemy.orm import sessionmaker

from persistency.connection import Base
from persistency.models.models import User
from tests.schemas_tests.users_tests_schemas import DEFAULT_ADMIN
from utils.providers.hash_provider import generate_hash

# Loading config to get database_url
DATABASE_TEST_URL = Config.DATABASE_TEST_URL
SCHEMA_TEST = "tests"

# Creating one async connection to database
test_engine = create_async_engine(DATABASE_TEST_URL)

async_session = sessionmaker(
    test_engine, expire_on_commit=False, class_=AsyncSession
)


def create_db(schema=SCHEMA_TEST):
    Base.metadata.create_all(bind=test_engine, schema=schema)


async def drop_db():
    async with async_session() as session:
        for table in Base.metadata.sorted_tables:
            if table.name in ["user"]:
                await session.execute(
                    f'TRUNCATE TABLE "{table.name}" RESTART IDENTITY CASCADE;'
                )
        user = User(**DEFAULT_ADMIN)
        user.password = generate_hash(user.password)
        session.add(user)
        await session.commit()


class DBSession:
    def __init__(self):
        self.session = async_session()

    async def __aenter__(self):
        return self.session

    async def __aexit__(self, exc_type, exc_val, exc_tb):
        await self.session.close()


async def get_test_db():
    return DBSession()
