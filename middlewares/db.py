from aiogram.dispatcher.middlewares import BaseMiddleware
from db.database import async_session


class DBMiddleware(BaseMiddleware):
    async def on_pre_process_message(self, message, data):
        session = async_session()
        data["db"] = session

    async def on_post_process_message(self, message, data, exception):
        session = data.get("db")
        if session:
            await session.close()
