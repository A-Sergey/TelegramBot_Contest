from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton


def genmarkup(data: list) -> InlineKeyboardMarkup:
    markup = InlineKeyboardMarkup()
    markup.row_width = 1
    for i in data:
        markup.add(InlineKeyboardButton(i[0], callback_data=i[0]))
    return markup

def to_pay(contest: str):
    markup = InlineKeyboardMarkup()
    markup.row_width = 1
    markup.add(InlineKeyboardButton("Внести плату", callback_data=f"pay_{contest}"))
    return markup
