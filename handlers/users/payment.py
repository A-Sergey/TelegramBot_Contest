from aiogram import types
import os

from main import dp, bot
from utils.db_api.db_quick_commands import get_contests, user_pay
from main import logging
import handlers.messages as MESSAGES


@dp.message_handler(commands=["terms"])
async def terms_command(message: types.Message):
    await message.reply("TEST_terms", reply=False)

#Payment receipt
@dp.callback_query_handler(lambda call: call.data.startswith('pay'))
async def pay_call(callback_query: types.CallbackQuery):
    await bot.answer_callback_query(callback_query.id)
    if "TEST" in os.getenv("PAYMENT_TEST"):
        await bot.send_message(
            callback_query.from_user.id, MESSAGES.test_payment
        )
    
    contest = get_contests(contest=callback_query.data[4:])[0]
    PRICE = types.LabeledPrice(label=contest[0], amount=int(contest[3]*100))
    await bot.send_invoice(
        callback_query.from_user.id,
        title=contest[0],
        description=contest[2],
        provider_token=os.getenv("PAYMENT_TEST"),
        currency="rub",
        photo_url=contest[1],
        photo_width=512,
        photo_size=512,
        is_flexible=False,
        prices=[PRICE],
        start_parameter="contest-bloggers",
        payload=contest[0]
    )

#Processing a payment
@dp.pre_checkout_query_handler(lambda query: True)
async def pre_checkout_query(pre_checkout_query: types.PreCheckoutQuery):
    await bot.answer_pre_checkout_query(pre_checkout_query.id, ok=True)

#processing a successful payment
@dp.message_handler(content_types=types.ContentType.SUCCESSFUL_PAYMENT)
async def successful_payment(message: types.Message):
    logging.info("successful payment:")
    payment = message.successful_payment.to_python()

    data = {
        "payment_id": payment["telegram_payment_charge_id"],
        "user_id": message.from_user.id,
        "username": message.from_user.username,
        "contestname": payment["invoice_payload"]
    }
    user_pay(data)
