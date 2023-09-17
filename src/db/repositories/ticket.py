from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from ..models import Ticket
from .abstract import Repository


class TicketRepo(Repository[Ticket]):
    """
    User repository for CRUD and other SQL queries
    """

    def __init__(self, session: AsyncSession):
        """
        Initialize user repository as for all users or only for one user
        """
        super().__init__(type_model=Ticket, session=session)

    async def new(
        self,
        id: str,
        role: str = "visitor",
        used_by: int = None,
        issued_by: int = None,
    ) -> Ticket:
        new_ticket = await self.session.merge(
            Ticket(id=id, role=role, used_by=used_by, issued_by=issued_by)
        )
        return new_ticket

    async def exists(self, ticket_id: str) -> bool:
        stmt = select(Ticket.id).where(Ticket.id == ticket_id).limit(1)
        if (await self.session.execute(stmt)).scalar_one_or_none():
            return True
        else:
            return False
