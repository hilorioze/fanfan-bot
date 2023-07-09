from sqlalchemy import select, func
from sqlalchemy.ext.asyncio import AsyncSession


class Requests(object):

    @classmethod
    async def get_one(cls, session: AsyncSession, whereclause):
        db_query = await session.execute(select(cls).where(whereclause))
        result = db_query.scalar_one_or_none()
        return result

    @classmethod
    async def get_many(cls, session: AsyncSession, whereclause):
        db_query = await session.execute(select(cls).where(whereclause))
        result = db_query.scalars().all()
        return result

    @classmethod
    async def get_range(cls, session: AsyncSession, start: int, end: int, sort_by):
        db_query = await session.execute(select(cls).order_by(sort_by).slice(start, end))
        return db_query.scalars().all()

    @classmethod
    async def count(cls, session: AsyncSession, whereclause) -> int:
        db_query = await session.execute(select(func.count()).select_from(cls).where(whereclause))
        count = db_query.scalar()
        return count
