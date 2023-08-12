from src.bot.ui.strings import buttons

main_menu_text = """Привет, {name}! Сейчас ты находишься в главном меню. Сюда всегда можно попасть по команде /start."""


helper_menu_text = f"""<s><b>{buttons.announce_mode}</b>
С помощью данного режима вы можете оперативно оповещать зрителей о том, что происходит на сцене</s>"""

org_menu_text = """<s><code>/role @ник роль</code>
Сменить роль пользователю.
Доступные роли: visitor, helper, org.</s>

<s><code>/info запрос</code>
Найти и вывести информацию о пользователе по номеру билета, @юзернейму или его Telegram ID.</s>

<b>Организаторы также могут использовать команды для волонтёров.</b>"""
