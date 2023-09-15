import asyncio
import io

import cv2
import numpy as np
from aiogram import Bot
from aiogram.enums import ContentType
from aiogram.types import Message
from aiogram_dialog import DialogManager, Window
from aiogram_dialog.widgets.input import MessageInput
from aiogram_dialog.widgets.kbd import SwitchTo
from aiogram_dialog.widgets.text import Const
from qreader import QReader

from src.bot.dialogs import states
from src.bot.dialogs.widgets import Title
from src.bot.ui import strings
from src.bot.utils.qr import proceed_qr_code

qreader = QReader()


async def indicator(bot: Bot, chat_id: int):
    while True:
        await bot.send_chat_action(chat_id=chat_id, action="choose_sticker")
        await asyncio.sleep(5)


async def on_photo_received(
    message: Message,
    message_input: MessageInput,
    manager: DialogManager,
):
    bot: Bot = manager.middleware_data["bot"]
    photo = await bot.get_file(file_id=message.photo[-1].file_id)
    indicator_task = asyncio.create_task(
        indicator(bot=bot, chat_id=manager.event.from_user.id)
    )
    binary = io.BytesIO()
    await bot.download_file(file_path=photo.file_path, destination=binary)
    image = cv2.cvtColor(
        cv2.imdecode(np.frombuffer(binary.read(), np.uint8), 1), cv2.COLOR_BGR2RGB
    )
    decoded_text = qreader.detect_and_decode(image=image)
    indicator_task.cancel()
    if decoded_text:
        await proceed_qr_code(
            manager=manager,
            db=manager.middleware_data["db"],
            qr_text=decoded_text[0],
            message=message,
        )
    else:
        await message.reply(text="Красивое фото, но QR-кода я на нём не вижу 😔")


qr_scanner_window = Window(
    Title(strings.titles.qr_scanner),
    Const("📸 Отправь фото с QR-кодом"),
    SwitchTo(text=Const(strings.buttons.back), state=states.MAIN.MAIN, id="back"),
    MessageInput(func=on_photo_received, content_types=ContentType.PHOTO),
    state=states.MAIN.QR_SCANNER,
)
