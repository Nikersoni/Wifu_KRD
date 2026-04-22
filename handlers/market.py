from aiogram import types
from loader import dp

@dp.message_handler(text="маркет")
async def market(message: types.Message):
    await message.answer("🛒 Маркет работает")
