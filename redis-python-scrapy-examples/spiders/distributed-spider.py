from urllib.parse import urlparse, urlunparse
from scrapy_redis.spiders import RedisSpider
from user_settings import redis_client, queue_name, set_name, time_to_shutdown, batch_size

class DistributedSpider(RedisSpider):
    name = "distributed_spider"
    redis_key = queue_name
    redis_batch_size = batch_size
    max_idle_time = time_to_shutdown

    def parse(self, response):

        title = response.css('h1.Text.Text__title1::text').get()
        rating = response.css('div.RatingStatistics__rating::text').get()
        description = response.css('span.Formatted::text').get()

        if(title and rating and description):
            yield {
                'title': title,
                'rating': rating,
                'description': description,
                'url': response.url,
            }

        for href in response.css('a::attr(href)').getall():
            if href:
                url = response.urljoin(href)
                url = url.split('#')[0]
                if url.startswith("https://www.goodreads.com/book/show/"):
                    if not redis_client.sismember(set_name, url):
                        redis_client.lpush(queue_name, url)
                        redis_client.sadd(set_name, url)
