import random
import time
from datetime import time


class PeopleGenerator:

    k = {
        time(0): 0,
        time(1): 0,
        time(2): 0,
        time(3): 0,
        time(4): 0,
        time(5): 0.3,
        time(6): 1,
        time(7): 1.7,
        time(8): 2,
        time(9): 2.2,
        time(10): 1.7,
        time(11): 1,
        time(12): 1,
        time(13): 1,
        time(14): 1,
        time(15): 1,
        time(16): 1,
        time(17): 2,
        time(18): 3,
        time(19): 5,
        time(20): 3,
        time(21): 2,
        time(22): 0.7,
        time(23): 0.5
    }

    def generate(self):
        while True:
            # тут нужно проверять сколько сейчас времени в нашей симуляции и умножать на соттв. k из словаря
            people = int(random.normalvariate(1000, 50) * k[])
            pflag = 1  # хз как надо делать флаг
            time.sleep(600)


