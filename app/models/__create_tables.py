from app.models.__base import Base

from asyncio import run
from app.dependencies import async_engine

metadata = Base.metadata


async def create_tables() -> None:
    import __models

    async with async_engine.begin() as conn:
        await conn.run_sync(metadata.drop_all)
        await conn.run_sync(metadata.create_all)

        tabelas = list(metadata.tables)

        print(f'\nTabelas {tabelas} criadas ...\n')


if __name__ == '__main__':

    run(create_tables())
