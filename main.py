from aiogram import executor
from loader import dp
import handlers

from db.database import engine
from db.models import Base


async def on_startup(dp):
    print("🚀 Bot starting...")

    try:
        async with engine.begin() as conn:
            await conn.run_sync(Base.metadata.create_all)

        print("✅ Database connected")

    except Exception as e:
        print(f"❌ DB ERROR: {e}")


async def on_shutdown(dp):
    print("🛑 Bot stopped")


if __name__ == "__main__":
    executor.start_polling(
        dp,
        on_startup=on_startup,
        on_shutdown=on_shutdown,
        skip_updates=True
    )
