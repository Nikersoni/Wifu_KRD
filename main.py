import logging
import os

from aiogram import Bot, Dispatcher, executor, types
from aiogram.contrib.fsm_storage.memory import MemoryStorage

from db.database import engine
from db.models import Base
from db.queries import get_or_create_user, get_balance, add_balance

logging.basicConfig(level=logging.INFO)

TOKEN = os.getenv("BOT_TOKEN")

bot = Bot(token=TOKEN)
dp = Dispatcher(bot, storage=MemoryStorage())


# 🚀 запуск
async def on_startup(dp):
    print("🚀 Bot started")

    # убираем конфликт
    await bot.delete_webhook(drop_pending_updates=True)

    # создаём таблицы
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)

    print("✅ DB ready")


# 👋 старт
@dp.message_handler(commands=["start"])
async def start_cmd(message: types.Message):
    await get_or_create_user(message.from_user.id)

    await message.answer(
        "👋 Добро пожаловать!\n"
        "Напиши: профиль"
    )


# 👤 профиль
@dp.message_handler(lambda m: m.text and m.text.lower() == "профиль")
async def profile(message: types.Message):
    user_id = message.from_user.id

    balance = await get_balance(user_id)

    await message.answer(
        f"👤 Профиль\n"
        f"💰 Баланс: {balance} монет"
    )


# 💰 тест команда
@dp.message_handler(commands=["add"])
async def add_money(message: types.Message):
    await add_balance(message.from_user.id, 100)

    await message.answer("💰 +100 монет")


if __name__ == "__main__":
    executor
