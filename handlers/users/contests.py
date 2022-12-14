from aiogram import types

from main import dp, bot
from utils.db_api.db_quick_commands import get_contests, have_payment
from keyboards.buttons import genmarkup, to_pay


# Output a list of current contests
@dp.message_handler(commands=["contests"])
async def out_current(message: types.Message):
    contests = get_contests()
    contests = list(filter(lambda contest: contest[4] == None, contests))
    if contests:
        await message.answer("Активные конкурсы:", reply_markup=genmarkup(contests))
    else:
        await message.answer("Отсутствуют активные конкурсы")


# Output of the list of completed contests
@dp.message_handler(commands=["finished_contests"])
async def out_completed(message: types.Message):
    contests = get_contests()
    contests = list(filter(lambda contest: contest[4] != None, contests))
    if contests:
        await message.answer("Завершенные конкурсы:", reply_markup=genmarkup(contests))
    else:
        await message.answer("Нет завершенных конкурсов")


# Output contest
@dp.callback_query_handler(lambda call: call.data.startswith("con_"))
async def contest_call(callback_query: types.CallbackQuery):
    await bot.answer_callback_query(callback_query.id)

    contests = get_contests()
    contest = tuple(
        filter(lambda contest: contest[0] == callback_query.data[4:], contests)
    )[0]

    if have_payment(callback_query.from_user.id, contest[0]):
        await bot.send_photo(
            callback_query.from_user.id,
            photo=contest[1],
            caption=f"Name: {contest[0]}\n"
            + f"Description: {contest[2]}\n"
            + f"Price: {contest[3]}\n"
            + f"{'Winner: ' + contest[4] if contest[4] else ''}",
            reply_markup=to_pay(callback_query.from_user.id, contest[0], True),
        )
    else:
        await bot.send_photo(
            callback_query.from_user.id,
            photo=contest[1],
            caption=f"Name: {contest[0]}\n"
            + f"Description: {contest[2]}\n"
            + f"Price: {contest[3]}\n"
            + f"{'Winner: ' + contest[4] if contest[4] else ''}",
            reply_markup=to_pay(callback_query.from_user.id, contest[0]),
        )
