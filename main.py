import logging, os
from aiogram import Bot, Dispatcher
from aiogram.contrib.fsm_storage.memory import MemoryStorage
import asyncio
from dotenv import load_dotenv


logging.basicConfig(level=logging.INFO)

load_dotenv()

API_TOKEN = os.getenv("TOKEN")
admins_id = os.getenv("ADMIN_ID").split(",")

storage = MemoryStorage()
loop = asyncio.get_event_loop()

bot = Bot(token=API_TOKEN)
dp = Dispatcher(bot, storage=storage, loop=loop)


async def on_startup(dp):
    from utils.notify_admins import startup_notify

    await startup_notify(dp)

    from utils.bot_commands import set_default_commands

    await set_default_commands(dp)

    logging.info("Бот запущен.")


if __name__ == "__main__":
    from aiogram import executor
    from handlers import dp

    executor.start_polling(dp, on_startup=on_startup, skip_updates=True)
