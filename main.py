from aiogram import executor
from loader import dp
import handlers

from db.database import engine
from db.models import Base

async def on_startup(dp):
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)

if __name__ == "__main__":
    executor.start_polling(dp, on_startup=on_startup)
