import operator

import jwt
from aiogram.types import Message
from aiogram_dialog import Dialog, DialogManager, Window
from aiogram_dialog.dialog import ChatEvent
from aiogram_dialog.widgets.input import ManagedTextInput, TextInput
from aiogram_dialog.widgets.kbd import (
    Cancel,
    Checkbox,
    Column,
    ManagedCheckbox,
    Radio,
    Start,
    SwitchTo,
    Url,
)
from aiogram_dialog.widgets.text import Const, Format, Jinja

from src.bot import TEMPLATES_DIR
from src.bot.dialogs import states
from src.bot.dialogs.widgets import Title
from src.bot.structures import UserRole
from src.bot.ui import strings
from src.config import conf
from src.db import Database

ID_TICKET_ROLE_PICKER = "ticket_role_picker"
ID_VOTING_ENABLED_CHECKBOX = "voting_enabled_checkbox"

with open(TEMPLATES_DIR / "stats.jinja2", "r", encoding="utf-8") as file:
    StatsTemplate = Jinja(file.read())


async def get_roles(**kwargs):
    return {"roles": list(map(lambda item: (item.value, item.label), UserRole))}


async def org_menu_getter(dialog_manager: DialogManager, db: Database, **kwargs):
    await dialog_manager.find(ID_VOTING_ENABLED_CHECKBOX).set_checked(
        await db.settings.get_voting_enabled()
    )
    jwt_token = jwt.encode(
        payload={"user_id": dialog_manager.event.from_user.id},
        key=conf.bot.secret_key,
        algorithm="HS256",
    )
    return {
        "web_panel_login_link": f"{conf.bot.web_panel_link}/auth?token={jwt_token}",
        "bot_info": (
            {
                "name": "🎫 Билетов",
                "value": await db.ticket.get_count(),
            },
            {
                "name": "👥 Пользователей",
                "value": await db.user.get_count(),
                "subs": (
                    {
                        "name": "👀 Зрителей",
                        "value": await db.user.get_count(role=UserRole.VISITOR),
                    },
                    {
                        "name": "📣 Волонтёров",
                        "value": await db.user.get_count(role=UserRole.HELPER),
                    },
                    {
                        "name": "⭐ Организаторов",
                        "value": await db.user.get_count(role=UserRole.ORG),
                    },
                ),
            },
            {
                "name": "💃 Выступлений",
                "value": await db.event.get_count(),
                "subs": (
                    {
                        "name": "🫣 Пропущено",
                        "value": await db.event.get_count(skipped=True),
                    },
                ),
            },
            {
                "name": "🧑‍🎤 Участников",
                "value": await db.participant.get_count(),
            },
            {
                "name": "🥈 Номинаций",
                "value": await db.nomination.get_count(),
                "subs": (
                    {
                        "name": "🥇 С голосованием",
                        "value": await db.nomination.get_count(
                            votable=True,
                        ),
                    },
                ),
            },
            {
                "name": "🗣️ Голосов",
                "value": await db.vote.get_count(),
            },
        ),
    }


async def switch_voting(
    event: ChatEvent, checkbox: ManagedCheckbox, manager: DialogManager
):
    db: Database = manager.middleware_data["db"]
    await db.settings.set_voting_enabled(
        manager.find(ID_VOTING_ENABLED_CHECKBOX).is_checked()
    )
    await db.session.commit()


async def add_new_ticket(
    message: Message,
    widget: ManagedTextInput,
    dialog_manager: DialogManager,
    data: str,
):
    db: Database = dialog_manager.middleware_data["db"]
    role = dialog_manager.find(ID_TICKET_ROLE_PICKER).get_checked()

    if await db.ticket.exists(data):
        await message.reply("⚠️ Билет с таким номером уже существует!")
        return

    new_ticket = await db.ticket.new(id=data, role=role, issued_by=message.from_user.id)
    db.session.add(new_ticket)
    await db.session.commit()

    await message.answer(
        f"""✅ Билет "{new_ticket.id}" с ролью {new_ticket.role} успешно добавлен!"""
    )
    await dialog_manager.switch_to(states.ORG.MAIN)


new_ticket_window = Window(
    Const("✔️ Отметьте роль для билета ниже и напишите его номер"),
    Column(
        Radio(
            Format("🔘 {item[1]}"),
            Format("⚪️ {item[1]}"),
            id=ID_TICKET_ROLE_PICKER,
            item_id_getter=operator.itemgetter(0),
            items="roles",
        ),
    ),
    TextInput(id="ticket_id", type_factory=str, on_success=add_new_ticket),
    SwitchTo(state=states.ORG.MAIN, id="org_menu", text=Const(strings.buttons.back)),
    getter=get_roles,
    state=states.ORG.NEW_TICKET,
)

org_menu = Window(
    Title(strings.titles.org_menu),
    Const("📊 <b>Статистика использования бота:</b>\n"),
    StatsTemplate,
    Url(
        text=Const("🌐 Перейти в панель администратора"),
        url=Format("{web_panel_login_link}"),
    ),
    Start(
        state=states.USER_MANAGER.MANUAL_USER_SEARCH,
        id="user_search",
        text=Const("🔍 Найти пользователя"),
    ),
    SwitchTo(
        state=states.ORG.NEW_TICKET,
        id="new_ticket",
        text=Const("🎫 Добавить новый билет"),
    ),
    Checkbox(
        Const("🔴 Выключить голосование"),
        Const("🟢 Включить голосование"),
        id=ID_VOTING_ENABLED_CHECKBOX,
        on_state_changed=switch_voting,
    ),
    Cancel(Const(strings.buttons.back)),
    state=states.ORG.MAIN,
    getter=org_menu_getter,
)

dialog = Dialog(org_menu, new_ticket_window)
