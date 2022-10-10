import logging
from aiogram import Dispatcher

from main import admins_id
from keyboards.buttons import kb


async def startup_notify(dp: Dispatcher):
    for admin in admins_id:
        try:
            text = "Бот запущен."
            await dp.bot.send_message(admin, text, reply_markup=kb)
        except Exception as err:
            logging.exception(err)
