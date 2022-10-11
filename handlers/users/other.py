from aiogram import types

from main import dp
from utils.db_api.db_quick_commands import register_user, select_user
from handlers import messages as MESSAGES


@dp.message_handler(commands=["start"])
async def command_start(message: types.Message):
    user = register_user(message)

    if user:
        await message.answer("Приветствуем в конкурсном боте 'удачная встреча'!")


@dp.message_handler(commands=["profile"])
async def show_profile(message: types.Message):
    user = select_user(message.from_user.id)
    if user != None:
        await message.answer(
            f"Ваш профиль\n"
            f"Name: {user.name}\n"
            f"Username: @{user.username}"
            f"\nAdmin"
            if user.admin
            else ""
        )
    else:
        await message.answer(f"@{message.from_user.username} Вы не зарегистрированы\n")


@dp.message_handler(commands=["help"])
async def show_profile(message: types.Message):
    await message.answer(MESSAGES.help)
