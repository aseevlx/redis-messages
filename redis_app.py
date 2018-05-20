import uuid
import string
import random

import redis

from config import *


redis = redis.StrictRedis(host=REDIS_HOST, port=REDIS_PORT, db=REDIS_DB)


class RedisApp(object):
    def __init__(self):
        """
        Initialize app with a randomly generated id
        """
        self.id = str(uuid.uuid4())

    def check_current_generator(self):
        """
        If not generator in redis - set it.
        Else return True if current process is a generator, or False, if not
        :return: boolean
        """
        current_generator = redis.get('generator')
        if not current_generator:
            current_generator = self.set_generator()
            print('I am a generator!')

        current_generator = current_generator.decode('utf-8')
        return current_generator == self.id

    def set_generator(self):
        """
        Set self id and expire it in 500 ms
        :return: None
        """
        redis.psetex('generator', 1000, self.id)
        return redis.get('generator')

    def get_message(self):
        """
        Get message and processes it
        :return: None
        """
        message = redis.lpop('messages')
        if not message:
            return

        message = message.decode('utf-8')
        # 5% of chance that message contains error
        is_message_correct = random.choices([True, False], [0.95, 0.05])
        if not is_message_correct:
            self.send_message('errors', message)
            return

        print(message)
        return

    def send_message(self, key='messages', value=''):
        """
        Create or append redis list value with a given key
        :param key: str, redis key
        :param value: str, value
        :return: None
        """
        if not value:
            value = self.generate_message()
        redis.lpush(key, value)

    @staticmethod
    def generate_message(length=15):
        """
        Generate random message from ascii symbols and strings
        :param length: int, length of string
        :return: None
        """
        return ''.join(random.choice(string.ascii_lowercase + string.digits)
                       for _ in range(0, random.randint(5, length)))

    @staticmethod
    def get_errors():
        """
        Get all messages with error from redis,
        print them and delete from redis
        :return: None
        """
        errors = redis.lrange('errors', 0, -1)
        redis.delete('errors')

        print('\n'.join([error.decode('utf-8') for error in errors]))

    def run(self):
        if self.check_current_generator():
            self.send_message()
            self.set_generator()
        else:
            self.get_message()
