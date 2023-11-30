import asyncio

from aiogram import F
from aiogram.types import Message
from aiogram_dialog import DialogManager, Window
from aiogram_dialog.widgets.input import TextInput
from aiogram_dialog.widgets.input.text import ManagedTextInput
from aiogram_dialog.widgets.kbd import SwitchTo
from aiogram_dialog.widgets.text import Const, Jinja

from src.bot.dialogs import states
from src.bot.dialogs.schedule.common import (
    ID_SCHEDULE_SCROLL,
    SchedulePaginator,
    schedule_getter,
    set_schedule_page,
    set_search_query,
)
from src.bot.dialogs.schedule.tools import notifier
from src.bot.dialogs.schedule.tools.common import (
    throttle_announcement,
)
from src.bot.dialogs.templates import schedule_list
from src.bot.structures import UserRole
from src.bot.ui import strings
from src.db import Database
from src.db.models import DBUser


async def proceed_input(
    message: Message,
    widget: ManagedTextInput,
    dialog_manager: DialogManager,
    data: str,
):
    db: Database = dialog_manager.middleware_data["db"]
    user: DBUser = dialog_manager.middleware_data["current_user"]

    # Проверяем права
    if user.role < UserRole.HELPER:
        await message.reply(strings.errors.access_denied)
        return

    # Поиск
    if not data.isnumeric():
        await set_search_query(message, widget, dialog_manager, data)
        return

    # Таймаут рассылки анонсов
    settings = await db.settings.get()
    time_left = await throttle_announcement(db, settings)
    if not time_left == 0:
        await message.answer(
            strings.errors.announce_too_fast.format(
                announcement_timeout=settings.announcement_timeout, time_left=time_left
            )
        )
        return

    # Сброс текущего выступления
    if int(data) == 0:
        current_event = await db.event.get_current()
        if current_event:
            current_event.current = None
            await db.session.commit()
        await message.reply("✅ Текущее выступление сброшено!")
        await dialog_manager.find(ID_SCHEDULE_SCROLL).set_page(0)
        await dialog_manager.switch_to(states.SCHEDULE.MAIN)
        return

    # Проверяем, что выступление существует и не скрыто
    new_current_event = await db.event.get(int(data))
    if not new_current_event:
        await message.reply("⚠️ Выступление не найдено!")
        return
    if new_current_event.skip:
        await message.reply("⚠️ Скрытое выступление нельзя отметить как текущее!")
        return

    # Получаем текущее выступление и снимаем с него флаг "текущее"
    current_event = await db.event.get_current()
    if current_event:
        if current_event == new_current_event:
            await message.reply("⚠️ Это выступление уже отмечено как текущее!")
            return
        current_event.current = None
        await db.session.flush([current_event])

    # Отмечаем выступление как текущее
    new_current_event.current = True
    await db.session.commit()

    # Выводим подтверждение
    await message.reply(
        f"✅ Выступление <b>{new_current_event.title}</b> отмечено как текущее"
    )

    # Запускаем проверку подписок
    asyncio.create_task(
        notifier.proceed_subscriptions(
            arq=dialog_manager.middleware_data["arq"], send_global_announcement=True
        )
    )

    # Отправляем пользователя на страницу с текущим выступлением
    await set_schedule_page(dialog_manager, new_current_event)
    await dialog_manager.switch_to(states.SCHEDULE.MAIN)


set_manual_event_window = Window(
    Const("<b>🔢 Укажите номер выступления, которое хотите отметить текущим:</b>"),
    Const("<i>(0 - сброс текущего выступления)</i>\n"),
    Jinja(schedule_list),
    Const(
        "🔍 <i>Для поиска отправьте запрос сообщением</i>",
        when=~F["dialog_data"]["search_query"],
    ),
    SchedulePaginator,
    TextInput(
        id="manual_event_input",
        type_factory=str,
        on_success=proceed_input,
    ),
    SwitchTo(state=states.SCHEDULE.MAIN, text=Const(strings.buttons.back), id="back"),
    state=states.SCHEDULE.ASK_MANUAL_EVENT,
    getter=schedule_getter,
)
