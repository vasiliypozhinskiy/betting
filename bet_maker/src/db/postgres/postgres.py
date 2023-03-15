from aiopg.sa import create_engine
import sqlalchemy as sa

from db.db import AbstractDB


class AsyncPostgres(AbstractDB):

    def __init__(self, connection_params: dict):
        self.connection_params = connection_params
        self._engine = None

    async def setup(self):
        self._engine = await create_engine(
            **self.connection_params
        )

    async def close(self):
        self._engine.close()

    async def get_by_id(self, table, id_):
        async with self._engine.acquire() as conn:
            row = await conn.execute(table.select().where(table.c.id == id_))

            return await row.fetchone()

    async def get_all(self, table):
        async with self._engine.acquire() as conn:
            rows = await conn.execute(table.select())

            return await rows.fetchall()

    async def get_columns(self, table, columns):
        async with self._engine.acquire() as conn:
            query = sa.sql.select(columns)

            rows = await conn.execute(query.select_from(table))
            return await rows.fetchall()

    async def insert(self, table: sa.Table, entity):
        async with self._engine.acquire() as conn:
            await conn.execute(table.insert(dict(entity)))

    async def update(self, table, id_, entity):
        async with self._engine.acquire() as conn:
            await conn.execute(table.update().where(table.c.id == id_).values(dict(entity)))
