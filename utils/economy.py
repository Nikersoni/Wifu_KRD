import time

DAILY_LIMIT = 500

def can_earn(user):
    now = int(time.time())
    if now - user.last_reset > 86400:
        user.daily_earned = 0
        user.last_reset = now
    return user.daily_earned < DAILY_LIMIT

def add_earn(user, amount):
    user.daily_earned += amount
