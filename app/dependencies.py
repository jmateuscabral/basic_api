from typing import Annotated, Generator

from fastapi import Header, HTTPException
from sqlalchemy.exc import IntegrityError
from sqlalchemy.ext.asyncio import AsyncSession, create_async_engine
from sqlalchemy.orm import sessionmaker

from app.configs import Settings

async_engine = create_async_engine(Settings.database_url)

SessionLocal = sessionmaker(
    autocommit=False,
    autoflush=False,
    expire_on_commit=False,
    class_=AsyncSession,
    bind=async_engine
)


async def get_session() -> Generator:
    db: AsyncSession = SessionLocal()
    try:
        yield db
    except HTTPException:
        await db.rollback()
    # finally:
    #     db.close()


# async def get_session():
#     # with SessionLocal() as session:
#     try:
#         yield SessionLocal()
#     except HTTPException:
#         SessionLocal().rollback()
#         raise
#     finally:
#         SessionLocal().close()


async def get_token_header(x_token: Annotated[str, Header()]):
    if x_token != "fake-super-secret-token":
        raise HTTPException(status_code=400, detail="X-Token header invalid")


async def get_query_token(token: str):
    if token != "jessica":
        raise HTTPException(status_code=400, detail="No Jessica token provided")
