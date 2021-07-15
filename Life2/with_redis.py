import redis


r = redis.StrictRedis(charset="utf-8",
                      decode_responses=True)
r.mset({"Croatia": "Zagreb", "Bahamas": "Nassau"})

data = r.get("Bahamas")
print(data)
