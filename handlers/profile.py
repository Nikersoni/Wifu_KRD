from aiogram import types
from loader import dp
from db.queries.users import get_or_create_user

@dp.message_handler(text="профиль")
async def profile(message: types.Message, db):
    user = await get_or_create_user(db, message.from_user.id)

    await message.answer(f"""
👤 Профиль

💰 {user.balance}
🎴 {user.cards_count}
🌳 {user.tree}
""")
