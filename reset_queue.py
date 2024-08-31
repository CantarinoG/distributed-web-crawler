from user_settings import redis_client, queue_name, set_name, seeds

def reset():
    redis_client.delete(queue_name)
    redis_client.delete(set_name)
    for url in seeds:
        redis_client.lpush(queue_name, url)

    print(f"Queue named {queue_name} clered.")
    print(f"Set named {set_name} clered.")
    print(f"Seeds added at the {queue_name} queue.")

reset()