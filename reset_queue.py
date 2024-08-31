from user_settings import redis_client, queue_name, set_name, key_words, result_set_name

def reset():
    redis_client.delete(queue_name)
    redis_client.delete(set_name)
    for key_word in key_words:
        redis_client.lpush(queue_name, f"https://www.goodreads.com/genres/{key_word}")
        redis_client.sadd(set_name, f"https://www.goodreads.com/genres/{key_word}")

    print(f"Queue named {queue_name} cleared.")
    print(f"Set named {set_name} cleared.")
    print(f"Seeds added at the {queue_name} queue.")

reset()