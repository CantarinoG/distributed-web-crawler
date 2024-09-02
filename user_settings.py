import redis
from db_secrets import redis_url

#Constantes usadas em outros arquivos:
redis_client = redis.from_url(redis_url)
queue_name = "to_scrap"
set_name = "already_added"

#Customização de parâmetros dos crawlers:
delay = 1
batch_size = 1
time_to_shutdown = 60

#Palavras-chaves para busca e nome do conjunto de resultados armazenados
key_words = ["literature"]
result_set_name = "books"