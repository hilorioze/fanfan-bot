from aiogram.types import CallbackQuery
from aiogram_dialog import Dialog, DialogManager, Window
from aiogram_dialog.widgets.kbd import Button, Start
from aiogram_dialog.widgets.text import Const, Format
from sqlalchemy.ext.asyncio import AsyncSession

from bot.db.models import Settings
from bot.dialogs import states
from bot.ui import strings


async def getter(session: AsyncSession, **kwargs):
    settings = await Settings.get_one(session, True)
    if settings.voting_enabled:
        switch_voting_text = strings.buttons.disable_voting
    else:
        switch_voting_text = strings.buttons.enable_voting
    return {"switch_voting_text": switch_voting_text}


async def switch_voting(
    callback: CallbackQuery, button: Button, manager: DialogManager
):
    session: AsyncSession = manager.middleware_data.get("session")
    settings = await Settings.get_one(session, True)
    settings.voting_enabled = not settings.voting_enabled
    await session.merge(settings)
    await session.commit()


org_menu = Window(
    Const("<b>🔧 Меню организатора</b>"),
    Const(" "),
    Const(strings.menus.org_menu_text),
    Button(
        Format("{switch_voting_text}"),
        id="switch_voting_button",
        on_click=switch_voting,
    ),
    Start(text=Const(strings.buttons.back), id="mm", state=states.MAIN.MAIN),
    state=states.ORG.MAIN,
    getter=getter,
)

dialog = Dialog(org_menu)
