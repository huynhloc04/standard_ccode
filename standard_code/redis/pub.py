#   https://viblo.asia/p/gioi-thieu-ve-pubsub-va-su-dung-python-va-redis-demo-pubsub-V3m5WbywlO7

import redis
import time

HOST = 'localhost'
PORT = '6379'
CHANNEL = 'test'

if __name__ == '__main__':
    r = redis.Redis(host=HOST, port=PORT)
    pub = r.publish(
        channel=CHANNEL,
        message='HelloWorld!'
    )
