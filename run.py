import time

from redis_app import RedisApp


app = RedisApp()

while True:
    app.run()
    time.sleep(0.5)
