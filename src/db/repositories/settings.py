from sqlalchemy import select, update
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import MappedColumn

from ..models import Settings
from .abstract import Repository


class SettingsRepo(Repository[Settings]):
    """
    User repository for CRUD and other SQL queries
    """

    def __init__(self, session: AsyncSession):
        """
        Initialize user repository as for all users or only for one user
        """
        super().__init__(type_model=Settings, session=session)

    async def exists(self) -> bool:
        if await self.session.get(Settings, 1):
            return True
        else:
            return False

    async def create(
        self, voting_enabled: bool, announcement_timestamp: float
    ) -> Settings:
        settings = await self.session.merge(
            Settings(
                voting_enabled=voting_enabled,
                announcement_timestamp=announcement_timestamp,
            )
        )
        return settings

    async def _get_setting(self, key: MappedColumn):
        return await self.session.scalar(select(key).where(Settings.id == 1).limit(1))

    async def get_voting_enabled(self) -> bool:
        return await self._get_setting(Settings.voting_enabled)

    async def get_announcement_timestamp(self) -> float:
        return await self._get_setting(Settings.announcement_timestamp)

    async def toggle_voting(self):
        await self.session.execute(
            update(Settings)
            .where(Settings.id == 1)
            .values(voting_enabled=not await self.get_voting_enabled())
        )
        await self.session.commit()

    async def set_announcement_timestamp(self, timestamp: float):
        await self.session.execute(
            update(Settings)
            .where(Settings.id == 1)
            .values(announcement_timestamp=timestamp)
        )
        await self.session.commit()
