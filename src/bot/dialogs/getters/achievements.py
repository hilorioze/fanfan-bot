from aiogram_dialog.widgets.text import Jinja

from src.bot import TEMPLATES_DIR
from src.db import Database
from src.db.models import User

with open(TEMPLATES_DIR / "achievements.jinja2", "r", encoding="utf-8") as file:
    AchievementsList = Jinja(file.read())


async def achievements_list(
    db: Database,
    achievements_per_page: int,
    page: int,
    user: User,
    show_ids: bool,
) -> dict:
    page = await db.achievement.paginate(
        page=page,
        achievements_per_page=achievements_per_page,
    )
    received_achievements = await db.achievement.check_user_achievements(
        user, page.items
    )
    return {
        "achievements": page.items,
        "pages": page.total,
        "received_achievements": received_achievements,
        "show_ids": show_ids,
    }
