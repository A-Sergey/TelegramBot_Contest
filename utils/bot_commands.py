from aiogram import types


async def set_default_commands(dp):
    await dp.bot.set_my_commands(
        [
            types.BotCommand("start", "Запустить бота"),
            types.BotCommand("profile", "Посмотреть профиль"),
            types.BotCommand("contests", "Конкурсы"),
            types.BotCommand("finished_contests", "Завершенные конкурсы"),
            types.BotCommand("help", "Справка"),
        ]
    )
