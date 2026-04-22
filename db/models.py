from sqlalchemy.orm import declarative_base
from sqlalchemy import Column, Integer, BigInteger

Base = declarative_base()


class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True)
    user_id = Column(BigInteger, unique=True)
    balance = Column(Integer, default=0)
