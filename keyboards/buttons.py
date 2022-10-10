from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton, ReplyKeyboardMarkup, KeyboardButton

from main import admins_id
from utils.db_api.schemas.table_db import session, Contest

kb = ReplyKeyboardMarkup(resize_keyboard=True)
kb.add(KeyboardButton("Добавить конкурс")).add(KeyboardButton("/Отмена"))

def genmarkup(data: list) -> InlineKeyboardMarkup:
    markup = InlineKeyboardMarkup()
    markup.row_width = 1
    for i in data:
        markup.add(InlineKeyboardButton(i[0], callback_data=f"con_{i[0]}"))
    return markup

def to_pay(user_id: int, contest: str, skip: bool = False):
    markup = InlineKeyboardMarkup()
    markup.row_width = 1
    contest_query = session.query(Contest).filter(Contest.name == contest).first()
    if not(skip):
        markup.add(InlineKeyboardButton("Внести плату", callback_data=f"pay_{contest}"))
    if not(contest_query.winner) and str(user_id) in admins_id:
        markup.add(InlineKeyboardButton("Выбрать победителя и закончить конкурс", callback_data=f"win_{contest}"))
    return markup
