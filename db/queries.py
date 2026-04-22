from db.database import async_session
from db.models import User
from sqlalchemy import select


async def get_or_create_user(user_id: int):
    async with async_session() as session:
        result = await session.execute(
            select(User).where(User.user_id == user_id)
        )
        user = result.scalar()

        if not user:
            user = User(user_id=user_id, balance=0)
            session.add(user)
            await session.commit()

        return user


async def get_balance(user_id: int):
    async with async_session() as session:
        result = await session.execute(
            select(User).where(User.user_id == user_id)
        )
        user = result.scalar()
        return user.balance if user else 0


async def add_balance(user_id: int, amount: int):
    async with async_session() as session:
        result = await session.execute(
            select(User).where(User.user_id == user_id)
        )
        user = result.scalar()

        if user:
            user.balance += amount
            await session.commit()
