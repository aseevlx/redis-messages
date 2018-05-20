import time
import sys

from redis_app import RedisApp


app = RedisApp()

if len(sys.argv) > 1 and sys.argv[1] == '-getErrors':
    app.get_errors()
else:
    while True:
        app.run()
        time.sleep(0.5)
