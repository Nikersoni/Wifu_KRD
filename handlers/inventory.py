from aiogram import types
from loader import dp
from sqlalchemy import select
from db.models import UserCard, Card

@dp.message_handler(text="инвентарь")
async def inv(message: types.Message, db):
    result = await db.execute(
        select(UserCard, Card)
        .join(Card, UserCard.card_id == Card.id)
        .where(UserCard.user_id == message.from_user.id)
    )

    rows = result.all()
    await message.answer(f"🎒 Карточек: {len(rows)}")
