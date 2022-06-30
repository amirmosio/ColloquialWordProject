import random
import time

import cachetools.func


@cachetools.func.ttl_cache(maxsize=None, ttl=4)
def test(seed):
    print("test")
    return str(seed) + ":" + str(random.random())


if __name__ == '__main__':
    for i in range(6):
        print(test(7))
        time.sleep(1)
    print("asdfadf")
    for i in range(6):
        print(test(15))
        print(test(7))
        time.sleep(1)
