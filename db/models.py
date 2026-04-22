from sqlalchemy import Column, Integer, BigInteger, String, Boolean, ForeignKey
from sqlalchemy.orm import declarative_base

Base = declarative_base()

class User(Base):
    __tablename__ = "users"

    id = Column(BigInteger, primary_key=True)

    balance = Column(Integer, default=0)
    fragments = Column(Integer, default=0)
    cards_count = Column(Integer, default=0)

    premium = Column(Boolean, default=False)
    tree = Column(Integer, default=0)

    active_card_id = Column(Integer)

    last_map = Column(Integer, default=0)
    last_bonus = Column(Integer, default=0)
    last_water = Column(Integer, default=0)

    daily_earned = Column(Integer, default=0)
    last_reset = Column(Integer, default=0)

    is_banned = Column(Boolean, default=False)


class Card(Base):
    __tablename__ = "cards"

    id = Column(Integer, primary_key=True)
    name = Column(String)
    rarity = Column(Integer)


class UserCard(Base):
    __tablename__ = "user_cards"

    id = Column(Integer, primary_key=True)
    user_id = Column(BigInteger, ForeignKey("users.id"))
    card_id = Column(Integer, ForeignKey("cards.id"))

    in_market = Column(Boolean, default=False)


class Market(Base):
    __tablename__ = "market"

    id = Column(Integer, primary_key=True)
    seller_id = Column(BigInteger)
    card_instance_id = Column(Integer)
    price = Column(Integer)


class CardImage(Base):
    __tablename__ = "card_images"

    card_id = Column(Integer, primary_key=True)
    file_id = Column(String)
