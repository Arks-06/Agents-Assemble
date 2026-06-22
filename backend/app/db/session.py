# handles database connection lifecycle
# configures the asynchronous engine and creates the session factory, ensuring every request has a reliable, isolated, and efficient link to PostgreSQL

from sqlalchemy.ext.asyncio import create_async_engine, async_sessionmaker
from app.core.config import settings

# controls tcp
engine = create_async_engine(settings.DATABASE_URL, echo=True)
# echo=True will print the raw SQL it generates 

# AsyncSessionLocal factory generates new database sessions for each user request
AsyncSessionLocal = async_sessionmaker(
    bind=engine, 
    expire_on_commit=False, 
    autoflush=False
)

async def get_db():
    async with AsyncSessionLocal() as session:
        yield session