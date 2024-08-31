from urllib.parse import urlparse
from scrapy_redis.spiders import RedisSpider
from user_settings import redis_client, queue_name, set_name, time_to_shutdown, batch_size

class DistributedSpider(RedisSpider):
    name = "distributed_spider"
    redis_key = queue_name
    redis_batch_size = batch_size
    max_idle_time = time_to_shutdown
            
    def parse(self, response):
        yield {
            'url': response.url,
        }
        base_domain = urlparse(response.url).netloc
        for href in response.css('a::attr(href)').getall():
            if href:
                url = response.urljoin(href)
                if urlparse(url).netloc == base_domain: #To verify if the URL is from the same domain. Just replace with 'True' if it should enable differente domains.
                    if not redis_client.sismember(set_name, url):
                        redis_client.lpush(queue_name, url)
                        redis_client.sadd(set_name, url)
