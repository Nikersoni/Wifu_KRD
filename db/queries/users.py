from sqlalchemy import select
from db.models import User

async def get_or_create_user(db, user_id):
    result = await db.execute(select(User).where(User.id == user_id))
    user = result.scalar()

    if not user:
        user = User(id=user_id)
        db.add(user)
        await db.commit()

    return user
