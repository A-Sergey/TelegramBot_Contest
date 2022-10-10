from aiogram import types

from main import dp
from utils.db_api.db_quick_commands import select_user


@dp.message_handler(commands=["profile"])
async def show_profile(message: types.Message):
    user = select_user(message.from_user.id)
    if user != None:
        await message.answer(
            f"Ваш профиль\n"
            f"Name: {user.name}\n"
            f"Username: @{user.username}"
            f"\nAdmin" if user.admin else ""
        )
    else:
        await message.answer(
            f"@{message.from_user.username} Вы не зарегистрированы\n"
        )
