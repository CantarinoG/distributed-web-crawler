import redis
from api_secrets import redis_url

redis_client = redis.from_url(redis_url)
queue_name = "to_scrap"
set_name = "already_added"
seeds = [
    "https://en.wikipedia.org"
]
delay = 0
batch_size = 1
time_to_shutdown = 60