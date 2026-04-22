from aiogram import types
from loader import dp

@dp.message_handler(lambda m: m.text and m.text.lower() == "профиль")
async def profile_test(message: types.Message):
    await message.answer("ПРОФИЛЬ РАБОТАЕТ ✅")
