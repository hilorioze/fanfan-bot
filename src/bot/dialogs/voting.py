import math
import operator
from typing import Any

from aiogram import F
from aiogram.types import CallbackQuery, Message
from aiogram_dialog import Dialog, DialogManager, Window
from aiogram_dialog.widgets.input import TextInput
from aiogram_dialog.widgets.input.text import ManagedTextInput
from aiogram_dialog.widgets.kbd import (
    Button,
    Cancel,
    Column,
    CurrentPage,
    FirstPage,
    LastPage,
    NextPage,
    PrevPage,
    Row,
    Select,
    StubScroll,
    SwitchTo,
)
from aiogram_dialog.widgets.text import Const, Format, Jinja
from sqlalchemy import and_
from sqlalchemy.orm import undefer

from src.bot.dialogs import states
from src.bot.dialogs.widgets import FormatTitle, Title
from src.bot.structures.userdata import UserData
from src.bot.ui import strings
from src.db import Database
from src.db.models import Event, Nomination, Participant, Vote

ID_NOMINATIONS_SCROLL = "nominations_scroll"
ID_VOTING_SCROLL = "voting_scroll"


# fmt: off
VotingList = Jinja(  # noqa: E501
    "{% for participant in participants %}"
        "{% if user_vote.participant_id == participant.id %}"
            "<b>"
        "{% endif %}"
        "<b>{{participant.id}}.</b> {{participant.title}} "
        "{% if (participant.votes_count % 10 == 1) and (participant.votes_count % 100 != 11) %}"  # noqa: E501
            "[{{participant.votes_count}} голос]"
        "{% elif (2 <= participant.votes_count % 10 <= 4) and (participant.votes_count % 100 < 10 or participant.votes_count % 100 >= 20) %}"  # noqa: E501
            "[{{participant.votes_count}} голоса]"
        "{% else %}"
            "[{{participant.votes_count}} голосов]"
        "{% endif %}"
        "{% if user_vote.participant_id == participant.id %}"
            "</b> ✅"
        "{% endif %}"
        "\n\n"
    "{% endfor %}")
# fmt: on


async def nominations_getter(dialog_manager: DialogManager, db: Database, **kwargs):
    user_data: UserData = await dialog_manager.middleware_data["state"].get_data()
    current_page = await dialog_manager.find(ID_NOMINATIONS_SCROLL).get_page()
    nominations = await db.nomination.get_page(
        current_page,
        user_data["items_per_page"],
        Nomination.votable.is_(True),
        order_by=Nomination.title,
    )
    nominations_list = []
    for nomination in nominations:
        nominations_list.append((nomination.title, nomination.id))
    return {
        "pages": dialog_manager.dialog_data["pages"],
        "nominations_list": nominations_list,
    }


async def participants_getter(dialog_manager: DialogManager, db: Database, **kwargs):
    user_data: UserData = await dialog_manager.middleware_data["state"].get_data()
    nomination_id = dialog_manager.dialog_data["nomination_id"]
    nomination = await db.nomination.get(nomination_id)

    terms = and_(
        Participant.nomination_id == nomination.id,
        Participant.event.any(Event.skip.isnot(True)),
    )
    pages = await db.participant.get_number_of_pages(user_data["items_per_page"], terms)
    current_page = await dialog_manager.find(ID_VOTING_SCROLL).get_page()
    participants = await db.participant.get_page(
        current_page,
        user_data["items_per_page"],
        query=terms,
        order_by=Participant.id,
        options=[undefer(Participant.votes_count)],
    )
    user_vote = await db.vote.get_by_where(
        and_(
            Vote.user_id == dialog_manager.event.from_user.id,
            Vote.participant.has(Participant.nomination_id == nomination_id),
        )
    )
    if user_vote:
        dialog_manager.dialog_data["user_vote_id"] = user_vote.id
    else:
        dialog_manager.dialog_data["user_vote_id"] = None
    return {
        "pages": pages,
        "nomination_title": nomination.title,
        "participants": participants,
        "user_vote": user_vote,
    }


async def open_nomination(
    callback: CallbackQuery, widget: Any, dialog_manager: DialogManager, item_id: str
):
    dialog_manager.dialog_data["nomination_id"] = item_id
    await dialog_manager.find(ID_VOTING_SCROLL).set_page(0)
    await dialog_manager.switch_to(states.VOTING.VOTING)


async def add_vote(
    message: Message,
    widget: ManagedTextInput,
    dialog_manager: DialogManager,
    data: int,
):
    db: Database = dialog_manager.middleware_data["db"]

    if not await db.settings.get_voting_enabled():
        await message.reply(strings.errors.voting_disabled)
        return
    if dialog_manager.dialog_data.get("user_vote_id"):
        await message.reply("⚠️ Вы уже голосовали в этой категории!")
        return
    if not message.text.isnumeric():
        await message.reply("Укажите номер выступающего!")
        return
    participant = await db.participant.get_by_where(
        and_(
            Participant.id == data,
            Participant.nomination_id == dialog_manager.dialog_data["nomination_id"],
            Participant.event.any(Event.skip.isnot(True)),
        )
    )
    if participant:
        await db.vote.new(message.from_user.id, participant.id)
        await db.session.commit()
    else:
        await message.reply("Неверно указан номер выступления")
        return


async def cancel_vote(callback: CallbackQuery, button: Button, manager: DialogManager):
    db: Database = manager.middleware_data["db"]
    if not await db.settings.get_voting_enabled():
        await callback.answer(strings.errors.voting_disabled)
        return
    user_vote = await db.vote.get(manager.dialog_data["user_vote_id"])
    await db.session.delete(user_vote)
    await db.session.commit()


nominations = Window(
    Title(strings.titles.voting),
    Const("Для голосования доступны следующие номинации:"),
    Column(
        Select(
            Format("{item[0]}"),
            id="nomination",
            item_id_getter=operator.itemgetter(1),
            items="nominations_list",
            on_click=open_nomination,
        ),
    ),
    StubScroll(ID_NOMINATIONS_SCROLL, pages="pages"),
    Row(
        FirstPage(scroll=ID_NOMINATIONS_SCROLL, text=Const("⏪")),
        PrevPage(scroll=ID_NOMINATIONS_SCROLL, text=Const("◀️")),
        CurrentPage(
            scroll=ID_NOMINATIONS_SCROLL, text=Format(text="{current_page1}/{pages}")
        ),
        NextPage(scroll=ID_NOMINATIONS_SCROLL, text=Const("▶️")),
        LastPage(scroll=ID_NOMINATIONS_SCROLL, text=Const("⏭️")),
        when=F["pages"] != 1,
    ),
    Cancel(Const(strings.buttons.back)),
    state=states.VOTING.NOMINATIONS,
    getter=nominations_getter,
)


voting = Window(
    FormatTitle("🎖️ Номинация {nomination_title}"),
    VotingList,
    Const("⌨️ Чтобы проголосовать, отправь номер участника.", when=~F["user_vote"]),
    StubScroll(ID_VOTING_SCROLL, pages="pages"),
    Row(
        FirstPage(scroll=ID_VOTING_SCROLL, text=Const("⏪")),
        PrevPage(scroll=ID_VOTING_SCROLL, text=Const("◀️")),
        CurrentPage(
            scroll=ID_VOTING_SCROLL, text=Format(text="{current_page1}/{pages}")
        ),
        NextPage(scroll=ID_VOTING_SCROLL, text=Const("▶️")),
        LastPage(scroll=ID_VOTING_SCROLL, text=Const("⏭️")),
        when=F["pages"] != 1,
    ),
    TextInput(
        id="vote_id_input",
        type_factory=int,
        on_success=add_vote,
    ),
    Button(
        Const("Отменить голос"),
        id="cancel_vote",
        when="user_vote",
        on_click=cancel_vote,
    ),
    SwitchTo(
        text=Const(strings.buttons.back),
        state=states.VOTING.NOMINATIONS,
        id="nominations",
    ),
    state=states.VOTING.VOTING,
    getter=participants_getter,
)


async def on_voting_start(start_data: Any, manager: DialogManager):
    user_data: UserData = await manager.middleware_data["state"].get_data()
    db: Database = manager.middleware_data["db"]
    manager.dialog_data["pages"] = math.ceil(
        await db.nomination.get_count(Nomination.votable.is_(True))
        / user_data["items_per_page"]
    )


dialog = Dialog(nominations, voting, on_start=on_voting_start)
