import logging
from aiogram import Bot, Dispatcher, executor, types
from aiogram.contrib.fsm_storage.memory import MemoryStorage
import os

logging.basicConfig(level=logging.INFO)

TOKEN = os.getenv("BOT_TOKEN")

bot = Bot(token=TOKEN)
dp = Dispatcher(bot, storage=MemoryStorage())


# 🚀 запуск
async def on_startup(dp):
    print("🚀 Bot started")

    # 💥 убираем конфликт
    await bot.delete_webhook(drop_pending_updates=True)


# ✅ тест команда
@dp.message_handler(commands=["start"])
async def start_cmd(message: types.Message):
    await message.answer("Бот работает ✅")


# ✅ текст
@dp.message_handler()
async def echo(message: types.Message):
    await message.answer(f"Ты написал: {message.text}")


if __name__ == "__main__":
    executor.start_polling(dp, on_startup=on_startup, skip_updates=True)
