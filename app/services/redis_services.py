import redis
import redis.client

# Configure Redis connection
#redis_client = redis.StrictRedis(host='redis-14581.c15.us-east-1-4.ec2.redns.redis-cloud.com:14581', port=14581, db=0, decode_responses=True)
redis_client = redis.Redis(
  host='redis-14581.c15.us-east-1-4.ec2.redns.redis-cloud.com',
  port=14581,
  password='Zt5ct1P5RL2ABezQhRVCttH0F0bPyqTi')

def add_token_to_blacklist(token: str, expire_minutes: int = 30):
    """
    Adds a token to the Redis blacklist with an expiration time.
    """
    redis_client.setex(token, expire_minutes * 60, 'blacklisted')

def is_token_blacklisted(token: str) -> bool:
    """
    Checks if a token is blacklisted.
    """
    return redis_client.exists(token)