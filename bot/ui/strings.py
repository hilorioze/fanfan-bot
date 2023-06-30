import random

quotes = [
    "С любовью, @Arutemu64 💖",
    "Бесконечность - не предел!",
    "ого ботовое 🤖🐈",
    "Магма течёт в наших венах, раскаляя сердца!",
    "Не содержит консервантов и ГМО!",
    "Ты сегодня неотразим(а)! ✨",
    "🪑",
    ":3",
    "Бип-бип 🤖",
    "До встречи на вершине мира!",
]

# buttons
announce_mode_button = "📢 Режим анонсов"
vote_button = '📄 Голосование'
helper_menu_button = '📣 Для волонтёров'
org_menu_button = '🔧 Для организаторов'
back_button = '◀️ Вернуться назад'
send_button = '📨 Отправить'
delete_button = '🗑️ Удалить'
next_button = "⏭️ Дальше"
open_channel = "📢 Канал с уведомлениями"
whats_new = "✨ Что нового?"
enable_voting = "🟢 Включить голосование"
disable_voting = "🔴 Выключить голосование"
show_schedule_button = "📅 Показать расписание"


# menus

def main_menu_text(first_name):
    text = f"""📃 <b>Главное меню</b>

Привет, {first_name}! Сейчас ты находишься в главном меню. Сюда всегда можно попасть по команде /menu.

Не забудь подписаться на <code>{open_channel}</code> чтобы получать уведомления о выступлениях!

<i>{random.choice(quotes)}</i>"""
    return text


helper_guide = f"""📣 <b>Для волонтёров доступны следующие функции:</b>

<b>{announce_mode_button}</b>
С помощью данного режима вы можете оперативно оповещать зрителей о том, что происходит на сцене
"""

org_guide = """🔧 <b>Для организаторов доступны следующие команды:</b>

<code>/role @ник роль</code>
Сменить роль пользователю.
Доступные роли: visitor, helper, org.

<code>/info запрос</code>
Найти и вывести информацию о пользователе по номеру билета, @юзернейму или его Telegram ID.

<b>Организаторы также могут использовать команды для волонтёров.</b>
"""

announce_mode_guide = f"""<b>📢 Режим анонсов</b>

Сейчас вы находитесь в режиме анонсов. В нем Вы можете быстро создавать уведомления о выступлениях и перерывах.
В большинстве случаев достаточно нажимать кнопку <code>{next_button}</code>.
Однако, если что-то пошло не по плану (перенос, другое время перерыва), придется создать анонс вручную.

Чтобы создать анонс вручную, отправьте его сообщением в формате:
<code>сейчас затем</code>
Вы можете указать либо номер события по расписанию (название загрузится автоматически), либо "перерыв", а затем длительность перерыва в минутах.
<b>Примеры сообщений:</b>
<code>64</code> - сейчас выступление 64
<code>63 64</code> - сейчас выступление 63, затем 64
<code>перерыв 30</code> - сейчас перерыв на 30 минут
<code>64 перерыв 60</code> - сейчас выступление 64, затем перерыв на 60 минут
<b>Перед рассылкой анонса вы сможете предпросмотреть его (и удалить, если ошиблись).</b>

Чтобы выйти из режима, нажмите на кнопку <code>{back_button}</code> под полем ввода сообщения (может скрываться за квадратной иконкой).
"""

# statuses

welcome = "Тебя приветствует (тестовый) (НЕ)официальный бот Нижегородского фестиваля анимации и фантастики FAN-FAN! 👋"
loading = "⌚ Загрузка..."
please_send_ticket = "🎟️ Для доступа к боту пришли номер своего билета"
registration_successful = "✅ Регистрация прошла успешно! Желаем хорошо провести время!"
voted_successfully = "✅ Вы успешно проголосовали!"


def role_changed_successfully(username, role):
    return f"✅ Вы успешно изменили роль пользователя <b>@{username}</b> на <b>{role}</b>"


unvoted = "✅ Вы успешно отменили свой голос! Теперь можете переголосовать."

# errors

announce_command_error = """❌ Произошла ошибка! Возможные варианты:
1. Нарушен синтаксис команды
2. Не найдено выступление под таким номером"""
ticket_not_found = "❌ Ваш билет не найден!"
ticket_used = "❌ Ваш билет был использован ранее!"
announcement_too_fast = """❌ С прошлого анонса не прошло 30 секунд!
Чтобы избежать повторов, рассылка анонсов возможна раз в 30 секунд."""
no_access = "❌ У вас нет доступа к этой команде!"
wrong_command_usage = "❌ Неправильное использование команды!"
performance_doesnt_exist = "❌ Такого выступления не существует!"
already_voted = "❌ Вы уже голосовали в этой категории!"
not_voted = "❌ Вы не голосовали за это выступление!"
voting_disabled = "❌ Голосование сейчас отключено"
