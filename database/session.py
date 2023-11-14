from sqlalchemy.ext.asyncio import async_sessionmaker, create_async_engine

DATABASE_URL = "sqlite+aiosqlite:///./database.db"

engine = create_async_engine(DATABASE_URL, connect_args={"check_same_thread": False}, echo=True)
Session = async_sessionmaker(engine)


async def get_db_session():
    db = Session()
    try:
        yield db
    finally:
        await db.close()
