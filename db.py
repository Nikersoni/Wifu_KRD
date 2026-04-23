import os
import random
from datetime import datetime

from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession
from sqlalchemy.orm import sessionmaker, declarative_base
from sqlalchemy import Column, Integer, BigInteger, String, select, DateTime

DB_URL = os.getenv("DATABASE_URL")

if DB_URL.startswith("postgresql://"):
    DB_URL = DB_URL.replace("postgresql://", "postgresql+asyncpg://", 1)

engine = create_async_engine(DB_URL, echo=False)

Session = sessionmaker(
    engine, class_=AsyncSession, expire_on_commit=False
)

Base = declarative_base()


# 👤 USERS
class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True)
    user_id = Column(BigInteger, unique=True)
    balance = Column(Integer, default=0)
    last_card = Column(DateTime)


# 🎴 CARDS
class Card(Base):
    __tablename__ = "cards"

    id = Column(Integer, primary_key=True)
    name = Column(String)
    rarity = Column(String)


# 🎒 USER CARDS
class UserCard(Base):
    __tablename__ = "user_cards"

    id = Column(Integer, primary_key=True)
    user_id = Column(BigInteger)
    card_id = Column(Integer)


# ===== ЛОГИКА =====

# получить/создать юзера
async def get_or_create_user(user_id):
    async with Session() as session:
        result = await session.execute(
            select(User).where(User.user_id == user_id)
        )
        user = result.scalar()

        if not user:
            user = User(user_id=user_id, balance=0)
            session.add(user)
            await session.commit()

        return user


# баланс
async def add_balance(user_id, amount):
    async with Session() as session:
        result = await session.execute(
            select(User).where(User.user_id == user_id)
        )
        user = result.scalar()

        user.balance += amount
        await session.commit()


# 🎴 дроп с шансами
RARITY_CHANCES = [
    ("⚪", 50),
    ("🟢", 25),
    ("🔵", 15),
    ("🟣", 8),
    ("🟡", 2),
]


def roll_rarity():
    roll = random.randint(1, 100)
    total = 0

    for rarity, chance in RARITY_CHANCES:
        total += chance
        if roll <= total:
            return rarity


async def get_card_by_rarity(rarity):
    async with Session() as session:
        result = await session.execute(
            select(Card).where(Card.rarity == rarity)
        )
        cards = result.scalars().all()

        if not cards:
            return None

        return random.choice(cards)


# 🎴 выдать карту (с КД)
async def give_card(user_id):
    async with Session() as session:
        result = await session.execute(
            select(User).where(User.user_id == user_id)
        )
        user = result.scalar()

        # ⏳ КД 4 часа
        if user.last_card:
            diff = (datetime.utcnow() - user.last_card).total_seconds()
            if diff < 14400:
                return None, int(14400 - diff)

        rarity = roll_rarity()
        card = await get_card_by_rarity(rarity)

        if not card:
            return None, None

        new_card = UserCard(
            user_id=user_id,
            card_id=card.id
        )

        user.last_card = datetime.utcnow()

        session.add(new_card)
        await session.commit()

        return (card, new_card.id), None


# 🎒 инвентарь
async def get_inventory(user_id):
    async with Session() as session:
        result = await session.execute(
            select(UserCard, Card)
            .join(Card, UserCard.card_id == Card.id)
            .where(UserCard.user_id == user_id)
        )
        return result.all()
