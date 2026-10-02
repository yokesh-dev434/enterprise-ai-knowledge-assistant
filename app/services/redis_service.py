
import json

import redis


redis_client = redis.Redis(
    host="localhost",
    port=6379,
    decode_responses=True
)


def get_conversation(session_id):
    return redis_client.lrange(
        session_id,
        0,
        -1
    )


def get_chat_sessions():
    return redis_client.hgetall(
        "chat_sessions"
    )


def remove_first_element(redis_key):
    redis_client.lpop(redis_key)


def slicing_window(redis_key):

    if redis_client.llen(redis_key) >= 5:
        remove_first_element(redis_key)


def add_conversation(
    session_id,
    user_message,
    ai_message
):

    conversation = {
        "user": user_message,
        "assistant": ai_message
    }

    slicing_window(session_id)

    redis_client.rpush(
        session_id,
        json.dumps(conversation)
    )

    # Store chat session information
    redis_client.hset(
        "chat_sessions",
        session_id,
        user_message
    )