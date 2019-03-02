import gevent.monkey
gevent.monkey.patch_all()

import logging
import os

import gevent
import redis

from abstract_feed import ApplicationBackend

REDIS_URL = os.environ.get('REDIS_URL', 'redis://localhost:6379')
REDIS_CHAN = 'chat'


class RedisBackend(ApplicationBackend):
    def __init__(self):
        super().__init__()
        self.redis = redis.from_url(REDIS_URL)
        self.pubsub = self.redis.pubsub()
        self.pubsub.subscribe(REDIS_CHAN)

    def __iter_data(self):
        for message in self.pubsub.listen():
            if message['type'] == 'message':
                data = message.get('data')
                logging.info(u'Sending message: {}'.format(data))
                yield data

    def run(self):
        """Listens for new messages in Redis, and sends them to clients."""
        if self.callback:        
            for data in self.__iter_data():
                for client in self.clients['Shiqan']:
                    self.callback(client, data)

    def start(self):
        gevent.spawn(self.run)
