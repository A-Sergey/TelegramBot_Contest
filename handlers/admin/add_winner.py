import logging
from random import choice
from aiogram import types

from main import dp, bot
from utils.db_api.schemas.table_db import session, Contest, User
from utils.db_api.db_quick_commands import get_user_in_contest


# Add winner
@dp.callback_query_handler(lambda call: call.data.startswith("win_"))
async def add_winner(callback_query: types.CallbackQuery):
    await bot.answer_callback_query(callback_query.id)
    users = get_user_in_contest(callback_query.data[4:])
    if users:
        winner = choice(users)
        contest = (
            session.query(Contest)
            .filter(Contest.name == callback_query.data[4:])
            .first()
        )
        user = session.query(User).filter(User.id == winner).first()
        contest.winner = user.name
        session.commit()
        await callback_query.message.delete_reply_markup()
        await bot.send_message(
            callback_query.from_user.id,
            f"Для конкурса {contest.name} выбран победитель {contest.winner}",
        )
        await bot.send_message(
            chat_id=user.id, text=f"Вы победили в конкурсе {contest.name}"
        )
    else:
        await bot.send_message(
            callback_query.from_user.id, "Пользователь не выбран, участников нет."
        )
        await bot.delete_message(
            callback_query.from_user.id, callback_query.message.message_id
        )
