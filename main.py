import logging
import os
from aiogram import Bot, Dispatcher, executor, types
from sqlalchemy import text

from db import *

logging.basicConfig(level=logging.INFO)

TOKEN = os.getenv("BOT_TOKEN")

bot = Bot(token=TOKEN)
dp = Dispatcher(bot)


# 🚀 старт
async def on_startup(dp):
    print("🚀 BOT START")

    await bot.delete_webhook(drop_pending_updates=True)

    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)

        # стартовые карты
        await conn.execute(text("""
        INSERT INTO cards (name, rarity) VALUES
        ('Asuna', '🟡'),
        ('Rem', '🟣'),
        ('Zero Two', '🔵'),
        ('Mikasa', '🟢'),
        ('Hinata', '⚪')
        ON CONFLICT DO NOTHING;
        """))

    print("✅ DB READY")


# 📩 сообщения
@dp.message_handler()
async def handler(message: types.Message):
    text = message.text.lower()
    user_id = message.from_user.id

    user = await get_or_create_user(user_id)

    if text == "/start":
        await message.answer(
            "👋 Добро пожаловать\n"
            "Команды:\n"
            "профиль\nкарта\nинвентарь"
        )

    elif text == "профиль":
        await message.answer(
            f"👤 Профиль\n"
            f"💰 Баланс: {user.balance}"
        )

    elif text == "карта":
        result, cooldown = await give_card(user_id)

        if cooldown:
            minutes = cooldown // 60
            await message.answer(f"⏳ Подожди {minutes} мин")
            return

        if not result:
            await message.answer("❌ Нет карт")
            return

        card, uid = result

        await message.answer(
            f"🎴 Новая карта!\n"
            f"🆔 {uid}\n"
            f"{card.name} {card.rarity}"
        )

    elif text == "инвентарь":
        items = await get_inventory(user_id)

        if not items:
            await message.answer("📭 Пусто")
            return

        msg = "🎒 Инвентарь:\n\n"

        for uc, c in items[:10]:
            msg += f"{uc.id} | {c.name} {c.rarity}\n"

        await message.answer(msg)

    elif text == "/add":
        await add_balance(user_id, 100)
        await message.answer("💰 +100")

    else:
        await message.answer("❓ Команда?")


if __name__ == "__main__":
    executor.start_polling(dp, on_startup=on_startup, skip_updates=True)
