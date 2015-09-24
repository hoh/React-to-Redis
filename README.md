# React-to-Redis
Propagate updates from your Redis hashes to the state of your React components
in Real-Time via WebSockets.

## How it works

The server-side component, `main.py`, will register to
[Redis Keyspace Notifications](http://redis.io/topics/notifications), and
forward new values via
[WebSockets](https://developer.mozilla.org/en-US/docs/Web/API/WebSockets_API)
to connected clients.

The Javascript library, `react-to-redis.js`, contains a
[React Mixin](https://facebook.github.io/react/docs/reusable-components.html#mixins)
that your new components can use to get their state updated. See `index.html`
for an example that uses this Mixin.

## Usage

Install Redis, for eg. on Ubuntu:
```
sudo apt-get install redis-server
```

Install library dependencies: [aiohttp]() and [asyncio_redis]():
```
pip install -r requirements.text
```

Launch the server.
```
python main.py
```

If all went well, you should be able to connect to http://127.0.0.1:8088/ in
a web browser. Or two web browsers. Maybe three ?

Finally, you can launch the demo `inject.py` script in another terminal. It
will update Redis with new data twice per second.
```
python inject.py
```

## Contribute

Comments and enhancements are welcome, just do a
[Pull-Request](https://github.com/hoh/React-to-Redis/pulls) or open an
[Issue](https://github.com/hoh/React-to-Redis/issues).
