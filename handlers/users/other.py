from aiogram import types

from main import dp, admins_id
from utils.db_api.db_quick_commands import register_user, select_user
from handlers import messages as MESSAGES
from keyboards.buttons import kb_auth


@dp.message_handler(commands=["start"])
async def command_start(message: types.Message):
    user_id = message.from_user.id
    if str(user_id) not in admins_id:
        if not select_user(user_id):
            await message.answer(
                "Проидите авторизацию по телефону", reply_markup=kb_auth
            )
        else:
            await message.answer("Вы авторизованы")
    else:
        await message.answer("Привет, админ!")


@dp.message_handler(content_types=types.ContentTypes.CONTACT)
async def command_auth(message: types.Message):
    user = register_user(message)
    if user:
        await message.answer(
            "Авторизация прошла успешно", reply_markup=types.ReplyKeyboardRemove()
        )
    else:
        await message.answer("Повторите авторизацию")


@dp.message_handler(commands=["profile"])
async def show_profile(message: types.Message):
    user = select_user(message.from_user.id)
    msg = None
    if str(message.from_user.id) in admins_id:
        msg = f"@{message.from_user.username} - админ\n"
    else:
        if user != None:
            msg = f"Ваш профиль\nName: {user.name}\nUsername: @{user.username}"
        else:
            msg = f"{message.from_user.first_name} Вы не зарегистрированы\n"
    await message.answer(msg)


@dp.message_handler(commands=["help"])
async def show_profile(message: types.Message):
    await message.answer(MESSAGES.help)
