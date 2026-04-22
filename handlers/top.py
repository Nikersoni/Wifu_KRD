from aiogram import types
from loader import dp

@dp.message_handler(text="топ")
async def top(message: types.Message):
    await message.answer("🏆 Топ работает")
