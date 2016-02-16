"""
Test app that injects new values in a Redis HSET every X seconds.
"""
import asyncio
import asyncio_redis
import random
from time import sleep

choices = ['Alice', 'Bob', 'Charlie', 'Daniel', 'Einstein', 'Francis']


@asyncio.coroutine
def example():
    # Create Redis connection
    connection = yield from asyncio_redis.Connection.create(host='10.0.3.44',
                                                            port=6379)

    while True:
        # Set a key
        yield from connection.hset('mykey', 'name',
                                   random.choice(choices))

        yield from connection.hset('mykey', 'value',
                                   str(random.randrange(100)))
        sleep(0.5)

    # When finished, close the connection.
    connection.close()

if __name__ == '__main__':
    loop = asyncio.get_event_loop()
    loop.run_until_complete(example())
