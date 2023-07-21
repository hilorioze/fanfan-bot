from typing import Any, Awaitable, Callable, Dict, Union

from aiogram import BaseMiddleware
from aiogram.types import CallbackQuery, Message, TelegramObject

from src.db import Database
from src.db.models import User


class UserData(BaseMiddleware):
    async def __call__(
        self,
        handler: Callable[[TelegramObject, Dict[str, Any]], Awaitable[Any]],
        event: Union[Message, CallbackQuery],
        data: Dict[str, Any],
    ) -> Any:
        db: Database = data["db"]
        user = await db.user.get_by_where(User.tg_id == data["event_from_user"].id)
        data["user"] = user
        return await handler(event, data)