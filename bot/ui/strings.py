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

org_guide = """🔧 <b>Для организаторов доступны следующие команды:</b>

<code>/role [@ник] [роль]</code>
Сменить роль пользователю.
Доступные роли: visitor, helper, org.

<b>Организаторы также могут использовать команды для волонтёров.</b>
    
"""

announce_mode_button = "📢 Режим анонсов"

helper_guide = f"""📣 <b>Для волонтёров доступны следующие функции:</b>

<b>{announce_mode_button}</b>
С помощью данного режима вы можете оперативно оповещать зрителей о том, что происходит на сцене
    
"""

announce_command_error = """❌ Произошла ошибка! Возможные варианты:
1. Нарушен синтаксис команды
2. Не найдено выступление под таким номером"""

enable_notifications_button = '🔊 Включить уведомления'
disable_notifications_button = '🔇 Выключить уведомления'
vote_button = '📄 Голосование'
helper_menu_button = '📣 Для волонтёров'
org_menu_button = '🔧 Для организаторов'
back_button = '◀️ Вернуться назад'

loading = "⌚ Загрузка..."

please_send_ticket = "Для доступа к боту пришли номер своего билета 🎟️"

send_button = '📨 Отправить'
delete_button = '🗑️ Удалить'

ticket_not_found = "❌ Ваш билет не найден! Если вы считаете, что это ошибка, обратитесь к @Arutemu64"
ticket_used = "❌ Ваш билет был использован ранее! Если вы считаете, что это ошибка, обратитесь к @Arutemu64"
registration_successful = "✅ Регистрация прошла успешно! Желаем хорошо провести время!"

welcome = "Тебя приветствует (тестовый) (НЕ)официальный бот Нижегородского фестиваля анимации и фантастики FAN-FAN! 👋"


def main_menu_text(first_name, random_quote):
    text = f"""📃 <b>Главное меню</b>

Привет, {first_name}! Сейчас ты находишься в главном меню. Сюда всегда можно попасть по команде /menu.

Не забудь включить уведомления кнопкой <code>🔊 Включить уведомления</code>

<i>{random_quote}</i>"""
    return text


announcement_too_fast = """❌ С прошлого анонса не прошло 30 секунд!
Чтобы избежать повторов, рассылать анонсы можно только раз в 30 секунд."""

announce_mode_guide = f"""<b>📢 Режим анонсов</b>

Чтобы создать анонс, отправьте его сообщением в формате:
<code>[сейчас] [затем - необязательно, но желательно]</code>
Вы можете указать либо номер выступления по расписанию (название загрузится автоматически), либо "перерыв", а затем длительность перерыва в минутах.
<b>Примеры сообщений:</b>
<code>64</code> - сейчас выступление 64
<code>63 64</code> - сейчас выступление 63, затем 64
<code>перерыв 30</code> - сейчас перерыв на 30 минут
<code>64 перерыв 60</code> - сейчас выступление 64, затем перерыв на 60 минут
<b>Перед рассылкой анонса вы сможете предпросмотреть его (и удалить, если ошиблись).</b>

Чтобы выйти из режима, нажмите на кнопку <code>{back_button}</code> под полем ввода сообщения (может скрываться за квадратной иконкой).
"""

no_access = "❌ У вас нет доступа к этой команде!"

wrong_command_usage = "❌ Неправильное использование команды!"
performance_doesnt_exist = "❌ Такого выступления не существует!"
already_voted = "❌ Вы уже голосовали в этой категории!"
voted_successfully = "✅ Вы успешно проголосовали!"


def role_changed_successfully(username, role):
    return f"✅ Вы успешно изменили роль пользователя <b>@{username}</b> на <b>{role}</b>"


update_menu_button = "🔄️ Обновить меню"

not_voted = "❌ Вы не голосовали за это выступление!"

unvoted = "✅ Вы успешно отменили свой голос! Теперь можете переголосовать."

voting_disabled = "❌ Голосование сейчас отключено"
enable_voting = "Включить голосование"
disable_voting = "Выключить голосование"