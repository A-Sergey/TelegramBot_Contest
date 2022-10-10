from aiogram import types

from main import dp
from utils.db_api.db_quick_commands import register_user


@dp.message_handler(commands=["start"])
async def command_start(message: types.Message):
    user = register_user(message)

    if user:
        await message.answer("Приветствуем в конкурсном боте 'удачная встреча'!")
