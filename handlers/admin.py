from aiogram import types
from loader import dp
from config import ADMINS

@dp.message_handler(commands=["admin"])
async def admin(message: types.Message):
    if message.from_user.id not in ADMINS:
        return
    await message.answer("Админка")
