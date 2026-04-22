from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession
from sqlalchemy.orm import sessionmaker, declarative_base
from sqlalchemy import Column, Integer, BigInteger, String, select
import os
import random

DB_URL = os.getenv("DATABASE_URL")

if DB_URL.startswith("postgresql://"):
    DB_URL = DB_URL.replace("postgresql://", "postgresql+asyncpg://", 1)

engine = create_async_engine(DB_URL, echo=False)

Session = sessionmaker(
    engine, class_=AsyncSession, expire_on_commit=False
)

Base = declarative_base()


# 👤 пользователь
class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True)
    user_id = Column(BigInteger, unique=True)
    balance = Column(Integer, default=0)


# 🎴 карты
class Card(Base):
    __tablename__ = "cards"

    id = Column(Integer, primary_key=True)
    name = Column(String)
    rarity = Column(String)


# 🎒 карты пользователя
class UserCard(Base):
    __tablename__ = "user_cards"

    id = Column(Integer, primary_key=True)
    user_id = Column(BigInteger)
    card_id = Column(Integer)


# 🔹 получить пользователя
async def get_user(user_id):
    async with Session() as session:
        result = await session.execute(
            select(User).where(User.user_id == user_id)
        )
        return result.scalar()


# 🔹 создать пользователя
async def create_user(user_id):
    async with Session() as session:
        user = User(user_id=user_id, balance=0)
        session.add(user)
        await session.commit()


# 🔹 добавить баланс
async def add_balance(user_id, amount):
    async with Session() as session:
        result = await session.execute(
            select(User).where(User.user_id == user_id)
        )
        user = result.scalar()

        if user:
            user.balance += amount
            await session.commit()


# 🎴 случайная карта
async def get_random_card():
    async with Session() as session:
        result = await session.execute(select(Card))
        cards = result.scalars().all()

        if not cards:
            return None

        return random.choice(cards)


# 🎴 выдать карту
async def give_card(user_id):
    async with Session() as session:
        result = await session.execute(select(Card))
        cards = result.scalars().all()

        if not cards:
            return None

        card = random.choice(cards)

        new_card = UserCard(
            user_id=user_id,
            card_id=card.id
        )

        session.add(new_card)
        await session.commit()

        return card, new_card.id


# 🎒 инвентарь
async def get_inventory(user_id):
    async with Session() as session:
        result = await session.execute(
            select(UserCard, Card)
            .join(Card, UserCard.card_id == Card.id)
            .where(UserCard.user_id == user_id)
        )

        return result.all()
