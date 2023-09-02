from aiogram_dialog import Dialog, DialogManager

from src.db import Database

from .common import EVENTS_PER_PAGE, set_schedule_page
from .main import schedule_main_window
from .subscriptions import (
    event_selector_window,
    set_subscription_counter_window,
    subscriptions_window,
)
from .tools import (
    set_manual_event_window,
    swap_events_window,
    toggle_event_skip_window,
)
from .utils.schedule_loader import ScheduleLoader


async def on_start_schedule(start_data: dict, manager: DialogManager):
    db: Database = manager.middleware_data["db"]

    current_event = await db.event.get_current()
    await set_schedule_page(manager, current_event)

    schedule_loader = ScheduleLoader(
        db=db,
        events_per_page=EVENTS_PER_PAGE,
    )
    manager.dialog_data["pages"] = await schedule_loader.get_pages_count()


dialog = Dialog(
    schedule_main_window,
    set_manual_event_window,
    swap_events_window,
    toggle_event_skip_window,
    subscriptions_window,
    event_selector_window,
    set_subscription_counter_window,
    on_start=on_start_schedule,
)
