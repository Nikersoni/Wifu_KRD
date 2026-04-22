from aiogram.dispatcher.middlewares import BaseMiddleware
from db.database import async_session


class DBMiddleware(BaseMiddleware):

    async def on_pre_process_message(self, message, data):
        session = async_session()
        data["db"] = session

    async def on_post_process_message(self, message, data, exception):
        # ✅ проверка что data — это dict
        if isinstance(data, dict):
            session = data.get("db")
            if session:
                await session.close()
