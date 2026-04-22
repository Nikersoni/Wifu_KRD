from aiogram import executor, types
from loader import dp
import handlers

from db.database import engine
from db.models import Base


# 🚀 Запуск
async def on_startup(dp):
    print("🚀 Bot starting...")

    try:
        async with engine.begin() as conn:
            await conn.run_sync(Base.metadata.create_all)

        print("✅ Database connected")

    except Exception as e:
        print(f"❌ DB ERROR: {e}")


# 🛑 Остановка
async def on_shutdown(dp):
    print("🛑 Bot stopped")


# 🔍 Лог входящих сообщений (в самом низу!)
@dp.message_handler(content_types=types.ContentType.TEXT)
async def debug_log(message: types.Message):
    print(f"MSG: {message.text}")


# ▶️ Запуск бота
if __name__ == "__main__":
    executor.start_polling(
        dp,
        on_startup=on_startup,
        on_shutdown=on_shutdown,
        skip_updates=True
    )
