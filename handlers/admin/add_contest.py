from aiogram.dispatcher.filters.state import State, StatesGroup
from aiogram.dispatcher import FSMContext
from aiogram import types
from aiogram.dispatcher.filters import Text

from main import dp, admins_id
from utils.db_api.db_quick_commands import add_contest


class FSMAdmin(StatesGroup):
    name = State()
    photo = State()
    description = State()
    price = State()


@dp.message_handler(state="*", commands="Отмена")
@dp.message_handler(Text(equals="Отмена", ignore_case=True), state="*")
async def cancel_handler(message: types.Message, state: FSMContext):
    current_state = await state.get_state()
    if current_state is None:
        return
    await state.finish()
    await message.reply("Ввод отменен")


@dp.message_handler(content_types=types.ContentType.TEXT, text="Добавить конкурс")
async def start_command(message: types.Message, state: FSMContext):
    if str(message.from_user.id) in admins_id:
        await FSMAdmin.name.set()
        await message.reply("Введите название конкурса")


@dp.message_handler(state=FSMAdmin.name)
async def add_name(message: types.Message, state: FSMContext):
    if str(message.from_user.id) in admins_id:
        async with state.proxy() as data:
            data["name"] = message.text
        await FSMAdmin.next()
        await message.reply("Добавте фото конкурса")


@dp.message_handler(content_types=["photo"], state=FSMAdmin.photo)
async def add_photo(message: types.Message, state: FSMContext):
    if str(message.from_user.id) in admins_id:
        async with state.proxy() as data:
            data["photo"] = message.photo[0].file_id
        await FSMAdmin.next()
        await message.reply("Введите описание конкурса")


@dp.message_handler(state=FSMAdmin.description)
async def add_description(message: types.Message, state: FSMContext):
    if str(message.from_user.id) in admins_id:
        async with state.proxy() as data:
            data["description"] = message.text
        await FSMAdmin.next()
        await message.reply("Введите взнос")


@dp.message_handler(state=FSMAdmin.price)
async def add_price(message: types.Message, state: FSMContext):
    if str(message.from_user.id) in admins_id:
        async with state.proxy() as data:
            data["price"] = float(message.text.replace(",", "."))

        async with state.proxy() as data:
            if add_contest(data):
                await message.answer("Конкурс добавлен")
            else:
                await message.answer("Конкурс не добавлен.\nНе коррекртные данные")
        await state.finish()
