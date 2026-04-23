import logging
import os
from aiogram import Bot, Dispatcher, executor, types
from sqlalchemy import text

from db import *

logging.basicConfig(level=logging.INFO)

TOKEN = os.getenv("BOT_TOKEN")

bot = Bot(token=TOKEN)
dp = Dispatcher(bot)


# 🚀 запуск
async def on_startup(dp):
    print("🚀 START OK")

    await bot.delete_webhook(drop_pending_updates=True)

    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)

        # добавляем стартовые карты (если пусто)
        await conn.execute(text("""
        INSERT INTO cards (name, rarity) VALUES
        ('Asuna', '🟡'),
        ('Rem', '🟣'),
        ('Zero Two', '🔵'),
        ('Mikasa', '🟢'),
        ('Hinata', '⚪')
        ON CONFLICT DO NOTHING;
        """))

    print("✅ DB OK")


# 🔥 основной обработчик
@dp.message_handler()
async def main_handler(message: types.Message):
    print("MESSAGE:", message.text)

    text_msg = message.text.lower()
    user_id = message.from_user.id

    # 👋 старт
    if text_msg == "/start":
        user = await get_user(user_id)

        if not user:
            await create_user(user_id)

        await message.answer(
            "👋 Добро пожаловать!\n"
            "Команды:\n"
            "профиль\n"
            "карта\n"
            "инвентарь"
        )

    # 👤 профиль
    elif text_msg == "профиль":
        user = await get_user(user_id)

        if not user:
            await create_user(user_id)
            user = await get_user(user_id)

        await message.answer(
            f"👤 Профиль\n"
            f"💰 Баланс: {user.balance}"
        )

    # 💰 тест деньги
    elif text_msg == "/add":
        await add_balance(user_id, 100)
        await message.answer("💰 +100 монет")

    # 🎴 получить карту
    elif text_msg == "карта":
        card = await give_card(user_id)

        if not card:
            await message.answer("❌ Нет карт в базе")
            return

        card_data, unique_id = card

        await message.answer(
            f"🎴 Ты получил карту!\n"
            f"🆔 ID: {unique_id}\n"
            f"⭐ {card_data.name} ({card_data.rarity})"
        )

    # 🎒 инвентарь
    elif text_msg == "инвентарь":
        items = await get_inventory(user_id)

        if not items:
            await message.answer("📭 Инвентарь пуст")
            return

        text = "🎒 Твои карты:\n\n"

        for uc, c in items[:10]:
            text += f"🆔 {uc.id} | {c.name} ({c.rarity})\n"

        await message.answer(text)

    else:
        await message.answer("❓ Неизвестная команда")


if __name__ == "__main__":
    executor.start_polling(dp, on_startup=on_startup, skip_updates=True)
