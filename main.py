import logging
import os
from aiogram import Bot, Dispatcher, executor, types

logging.basicConfig(level=logging.INFO)

TOKEN = os.getenv("BOT_TOKEN")

bot = Bot(token=TOKEN)
dp = Dispatcher(bot)


async def on_startup(dp):
    print("🚀 START OK")
    await bot.delete_webhook(drop_pending_updates=True)


# 🔥 ЛОВИТ ВСЁ БЕЗ УСЛОВИЙ
@dp.message_handler()
async def test(message: types.Message):
    print("MESSAGE:", message.text)

    if message.text == "/start":
        await message.answer("СТАРТ РАБОТАЕТ")

    elif message.text.lower() == "профиль":
        await message.answer("ПРОФИЛЬ РАБОТАЕТ")

    else:
        await message.answer("НЕИЗВЕСТНАЯ КОМАНДА")


if __name__ == "__main__":
    executor.start_polling(dp, on_startup=on_startup, skip_updates=True)
