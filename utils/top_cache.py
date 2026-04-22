import time

CACHE = {"data": None, "time": 0}

def expired():
    return time.time() - CACHE["time"] > 21600

def set_cache(data):
    CACHE["data"] = data
    CACHE["time"] = time.time()
