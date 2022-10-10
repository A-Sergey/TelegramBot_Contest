from aiogram import types

from main import dp, bot
from utils.db_api.db_quick_commands import get_contests, have_payment
from keyboards.buttons import genmarkup, to_pay 

#Output a list of current contests
@dp.message_handler(commands=["contests"])
async def test_test(message: types.Message):
    contests = get_contests()
    contests = (list(filter(lambda contest: contest[4] == None, contests)))
    await message.answer("Список:", reply_markup=genmarkup(contests))

#Output of the list of completed contests
@dp.message_handler(commands=["finished_contests"])
async def test_test(message: types.Message):
    contests = get_contests()
    contests = (list(filter(lambda contest: contest[4] != None, contests)))
    await message.answer("Список:", reply_markup=genmarkup(contests))

#Output contest
@dp.callback_query_handler(lambda call: not(call.data.startswith('pay')))
async def contest_call(callback_query: types.CallbackQuery):
    await bot.answer_callback_query(callback_query.id)
    
    contests = get_contests()
    contest = tuple(
        filter(lambda contest: contest[0] == callback_query.data, contests)
    )[0]
    
    if have_payment(callback_query.from_user.id, contest[0]):
        await bot.send_photo(
            callback_query.from_user.id,
            photo=contest[1],
            caption=f"Name: {contest[0]}\n" +
            f"Description: {contest[2]}\n" +
            f"Price: {contest[3]}\n" +
            f"{'Winner: @' + contest[4] if contest[4] else ''}",
        )        
    else:
        await bot.send_photo(
            callback_query.from_user.id,
            photo=contest[1],
            caption=f"Name: {contest[0]}\n" +
            f"Description: {contest[2]}\n" +
            f"Price: {contest[3]}\n" +
            f"{'Winner: @' + contest[4] if contest[4] else ''}",
            reply_markup=to_pay(contest[0])
        )
