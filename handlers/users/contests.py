import logging
from aiogram import types
from random import choice

from main import dp, bot
from utils.db_api.db_quick_commands import get_contests, have_payment, get_user_in_contest
from keyboards.buttons import genmarkup, to_pay 
from utils.db_api.schemas.table_db import session, Contest

#Output a list of current contests
@dp.message_handler(commands=["contests"])
async def out_current(message: types.Message):
    contests = get_contests()
    contests = (list(filter(lambda contest: contest[4] == None, contests)))
    await message.answer("Список:", reply_markup=genmarkup(contests))

#Output of the list of completed contests
@dp.message_handler(commands=["finished_contests"])
async def out_completed(message: types.Message):
    contests = get_contests()
    contests = (list(filter(lambda contest: contest[4] != None, contests)))
    await message.answer("Список:", reply_markup=genmarkup(contests))

#Output contest
@dp.callback_query_handler(lambda call: call.data.startswith('con_'))
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
            caption=f"Name: {contest[0]}\n" +
            f"Description: {contest[2]}\n" +
            f"Price: {contest[3]}\n" +
            f"{'Winner: @' + contest[4] if contest[4] else ''}",
            reply_markup=to_pay(callback_query.from_user.id, contest[0], True)
        )        
    else:
        await bot.send_photo(
            callback_query.from_user.id,
            photo=contest[1],
            caption=f"Name: {contest[0]}\n" +
            f"Description: {contest[2]}\n" +
            f"Price: {contest[3]}\n" +
            f"{'Winner: @' + contest[4] if contest[4] else ''}",
            reply_markup=to_pay(callback_query.from_user.id, contest[0])
        )

#Add winner
@dp.callback_query_handler(lambda call: call.data.startswith('win_'))
async def add_winner(callback_query: types.CallbackQuery):
    await bot.answer_callback_query(callback_query.id)
    users = get_user_in_contest(callback_query.data[4:])
    if users:
        winner = choice(users)
        contest = session.query(Contest).filter(Contest.name == callback_query.data[4:]).first()
        contest.winner = winner
        session.commit()
        logging.info(f"Для конкурса {contest.name} выбран победитель {winner}")
    else:
        logging.warning("Пользователь не выбран, участников нет.")
