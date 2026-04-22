import time

ACTIONS = {}

def anti_spam(user_id, action, delay=2):
    now = time.time()
    key = (user_id, action)

    last = ACTIONS.get(key, 0)
    if now - last < delay:
        return False

    ACTIONS[key] = now
    return True
