import random

from aiogram.types import ErrorEvent
from aiogram_dialog import DialogManager, Window
from aiogram_dialog.widgets.kbd import Row, Start, SwitchTo, Url
from aiogram_dialog.widgets.text import Const, Format

from src.bot.dialogs import states
from src.bot.structures import Role
from src.bot.ui import strings
from src.config import conf
from src.db.models import User


async def getter(dialog_manager: DialogManager, user: User, **kwargs):
    if type(dialog_manager.event) is ErrorEvent:
        if dialog_manager.event.update.message:
            name = dialog_manager.event.update.message.from_user.first_name
        elif dialog_manager.event.update.callback_query:
            name = dialog_manager.event.update.callback_query.from_user.first_name
    else:
        name = dialog_manager.event.from_user.first_name
    is_helper = user.role == Role.HELPER
    is_org = user.role == Role.ORG
    if is_org:
        is_helper = True
    random_quote = random.choice(strings.quotes)
    return {
        "name": name,
        "is_helper": is_helper,
        "is_org": is_org,
        "random_quote": random_quote,
    }


main = Window(
    Const("<b>📃 Главное меню</b>"),
    Const(text=" "),
    Format(strings.menus.main_menu_text),
    Const(text=" "),
    Format("{random_quote}"),
    Url(
        text=Const(strings.buttons.changelog_channel),
        url=Const("https://t.me/fanfan_bot_dev_notes"),
    ),
    Url(
        text=Const(strings.buttons.notifications_channel),
        url=Const(conf.bot.channel_link),
    ),
    Row(
        Start(
            text=Const(strings.buttons.show_schedule),
            state=states.MAIN.SCHEDULE,
            id="schedule",
            data={"show_current_page": True},
        ),
        SwitchTo(
            Const(strings.buttons.activities_menu),
            id="activities",
            state=states.MAIN.ACTIVITIES,
        ),
    ),
    Start(
        text=Const(strings.buttons.voting), state=states.VOTING.NOMINATIONS, id="voting"
    ),
    Row(
        Start(
            text=Const(strings.buttons.helper_menu),
            id="helper_menu",
            when="is_helper",
            state=states.HELPER.MAIN,
        ),
        Start(
            text=Const(strings.buttons.org_menu),
            id="org_menu",
            when="is_org",
            state=states.ORG.MAIN,
        ),
    ),
    state=states.MAIN.MAIN,
    getter=getter,
)
