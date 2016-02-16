# Copyright (c) 2016, Hugo Herter
# All rights reserved.

"""
This HTTP Server will publish all changes to Redis HSETs to connected clients
via websockets.
"""

import asyncio
import aiohttp
from aiohttp import web
import asyncio_redis
import json
import logging

from .here import Here
here = Here(__file__)

# Settings
REDIS = dict(host='127.0.0.1', port=6379)
REDIS_KEY = 'mykey'
SERVE_ON = dict(host='0.0.0.0', port=8088)

# Enable logging
logging.getLogger().addHandler(logging.StreamHandler())
logging.getLogger().setLevel(logging.DEBUG)

# Global list of websocket clients
clients = []


@asyncio.coroutine
def redis_changes():
    # Create connection
    connection = yield from asyncio_redis.Connection.create(**REDIS)
    connection2 = yield from asyncio_redis.Connection.create(**REDIS)

    # Create subscriber.
    subscriber = yield from connection.start_subscribe()

    # Subscribe to channel.
    yield from subscriber.subscribe(["__keyevent@0__:hset"])

    # Inside a while loop, wait for incoming events.
    while True:
        reply = yield from subscriber.next_published()
        print('Received: ', repr(reply.value), 'on channel', reply.channel)
        promise = yield from connection2.hgetall(reply.value)
        print('-> Promise:', promise)
        value = yield from promise.asdict()
        print('-> Value:', value)
        print(clients)
        for ws in clients:
            ws.send_str(json.dumps(value))

    # When finished, close the connection.
    connection.close()
    connection2.close()

@asyncio.coroutine
def index_handler(request):
    text = here.open('index.html', 'r').read()
    return web.Response(body=text.encode('utf-8'))


@asyncio.coroutine
def jsapp_handler(request):
    text = here.open('react-to-redis.js', 'r').read()
    return web.Response(body=text.encode('utf-8'))


@asyncio.coroutine
def websocket_handler(request):
    ws = web.WebSocketResponse()
    clients.append(ws)
    ws.start(request)

    connection = yield from asyncio_redis.Connection.create(**REDIS)

    while True:
        try:
            msg = yield from ws.receive()
        except RuntimeError:
            clients.remove(ws)
            print('client disconnected')
            break

        if msg.tp == aiohttp.MsgType.text:
            print(msg.data)
            if msg.data == 'close':
                yield from ws.close()
            else:
                promise = yield from connection.hgetall(REDIS_KEY)
                value = yield from promise.asdict()
                ws.send_str(json.dumps(value))
        elif msg.tp == aiohttp.MsgType.close:
            print('websocket connection closed')
        elif msg.tp == aiohttp.MsgType.error:
            print('ws connection closed with exception %s',
                  ws.exception())

    connection.close()
    return ws


@asyncio.coroutine
def init(loop):
    app = web.Application(loop=loop)
    app.router.add_route('GET', '/', index_handler)
    app.router.add_route('GET', '/ws', websocket_handler)
    app.router.add_route('GET', '/react-to-redis.js', jsapp_handler)

    srv = yield from loop.create_server(app.make_handler(), **SERVE_ON)
    print("Server started at http://{server}:{port}".format(**SERVE_ON))
    return srv


def main():
    loop = asyncio.get_event_loop()
    loop.run_until_complete(asyncio.gather(init(loop), redis_changes()))
    try:
        loop.run_forever()
    except KeyboardInterrupt:
        pass


if __name__ == '__main__':
    main()
