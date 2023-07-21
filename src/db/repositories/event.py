from sqlalchemy.ext.asyncio import AsyncSession

from ..models import Event
from .base import Repository


class EventRepo(Repository[Event]):
    """
    User repository for CRUD and other SQL queries
    """

    def __init__(self, session: AsyncSession):
        """
        Initialize user repository as for all users or only for one user
        """
        super().__init__(type_model=Event, session=session)

    async def new(self):  # TODO
        return
