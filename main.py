import logging
import os
from aiogram import Bot, Dispatcher, executor, types

from db import *

logging.basicConfig(level=logging.INFO)

TOKEN = os.getenv("BOT_TOKEN")

bot = Bot(token=TOKEN)
dp = Dispatcher(bot)


# 🚀 запуск
async def on_startup(dp):
    print("🚀 START OK")

    await bot.delete_webhook(drop_pending_updates=True)

    # создаём таблицы
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)

    print("✅ DB OK")


# 🔥 ОСНОВНОЙ ХЕНДЛЕР
@dp.message_handler()
async def main_handler(message: types.Message):
    print("MESSAGE:", message.text)

    text = message.text.lower()
    user_id = message.from_user.id

    # 👋 старт
    if text == "/start":
        user = await get_user(user_id)

        if not user:
            await create_user(user_id)

        await message.answer(
            "👋 Добро пожаловать!\n"
            "Напиши: профиль"
        )

    # 👤 профиль
    elif text == "профиль":
        user = await get_user(user_id)

        if not user:
            await create_user(user_id)
            user = await get_user(user_id)

        await message.answer(
            f"👤 Профиль\n"
            f"💰 Баланс: {user.balance}"
        )

    # 💰 тест деньги
    elif text == "/add":
        await add_balance(user_id, 100)

        await message.answer("💰 +100 монет")

    else:
        await message.answer("❓ Неизвестная команда")


if __name__ == "__main__":
    executor.start_polling(dp, on_startup=on_startup, skip_updates=True)
