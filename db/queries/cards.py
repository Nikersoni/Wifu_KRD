import random
from sqlalchemy import select
from db.models import Card, UserCard

CHANCES = [(1,62),(2,24),(3,10),(4,3.5),(5,0.5)]

def roll():
    r = random.uniform(0,100)
    s = 0
    for rarity,ch in CHANCES:
        s += ch
        if r <= s:
            return rarity

async def get_card(db):
    rarity = roll()
    result = await db.execute(select(Card).where(Card.rarity == rarity))
    cards = result.scalars().all()
    return random.choice(cards), rarity

async def add_card(db, user_id, card_id):
    uc = UserCard(user_id=user_id, card_id=card_id)
    db.add(uc)
    await db.commit()
    return uc
