import time, random
from aiogram import types
from loader import dp
from db.queries.users import get_or_create_user
from db.queries.cards import get_card, add_card
from utils.guard import anti_spam
from utils.economy import can_earn, add_earn

@dp.message_handler(text="карта")
async def map_cmd(message: types.Message, db):
    user = await get_or_create_user(db, message.from_user.id)

    if not anti_spam(user.id, "map"):
        return

    now = int(time.time())
    if now - user.last_map < 14400:
        await message.answer("⏳ Подожди")
        return

    card, rarity = await get_card(db)
    await add_card(db, user.id, card.id)

    coins = random.randint(5,10)

    if not can_earn(user):
        coins = 0

    user.balance += coins
    user.cards_count += 1
    user.last_map = now

    add_earn(user, coins)

    await db.commit()

    await message.answer(f"🎴 {card.name}\n+{coins} монет")
