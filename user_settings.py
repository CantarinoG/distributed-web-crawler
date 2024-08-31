import redis
from api_secrets import redis_url

redis_client = redis.from_url(redis_url)
queue_name = "to_scrap"
set_name = "visited"
seeds = [
    "https://quotes.toscrape.com/page/1/"
]