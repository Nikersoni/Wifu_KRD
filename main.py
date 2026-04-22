import logging
from aiogram import Bot, Dispatcher, executor, types
from aiogram.contrib.fsm_storage.memory import MemoryStorage
import os
from db.queries import get_or_create_user, get_balance, add_balance

from db.database import engine
from db.models import Base

logging.basicConfig(level=logging.INFO)

TOKEN = os.getenv("BOT_TOKEN")

bot = Bot(token=TOKEN)
dp = Dispatcher(bot, storage=MemoryStorage())


async def on_startup(dp):
    print("🚀 Bot started")

    await bot.delete_webhook(drop_pending_updates=True)

    # ✅ создаём таблицы
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)

    print("✅ DB ready")


@dp.message_handler(commands=["start"])
async def start_cmd(message: types.Message):
    await message.answer("Бот с БД работает ✅")


if __name__ == "__main__":
    executor.start_polling(dp, on_startup=on_startup, skip_updates=True)
